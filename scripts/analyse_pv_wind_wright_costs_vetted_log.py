"""
Analyse PV and wind cumulative installed capacity by net-zero-by-2070 group,
and estimate PV and wind technology costs using Wright's law / experience curves.

This version keeps only scenarios with Vetting|SCI 2025 == "ok" by default,
because those are the scenarios verified by the SCI vetting procedure.

This version reads your local historical cost files directly:
    - solar-pv-prices.csv
    - costs-wind-over-time.csv

Both cost projections are reported in USD/kW.

Important unit note
-------------------
The wind file usually reports Technology cost in USD/kW.
The solar file from OWID often reports "Solar PV module cost" in USD/W, even
when the desired output is USD/kW. The script therefore uses automatic unit
detection by default:
    - if costs look like USD/W, it multiplies by 1000;
    - otherwise it keeps them as USD/kW.
You can override this with --pv-cost-input-unit or --wind-cost-input-unit.

Wright's law / one-factor learning curve
----------------------------------------
    cost_t = cost_0 * (experience_t / experience_0) ** (-b)

where:
    - cost_t is technology cost in USD/kW
    - experience_t is cumulative deployment, proxied here by installed capacity
    - b is the Wright learning exponent
    - learning rate = 1 - 2 ** (-b)

The script estimates one learning exponent for PV and one for wind by matching
historical costs to the mean SCI capacity trajectory over overlapping years.
Then it projects costs to 2070 separately for:
    - net_zero_by_2070
    - not_net_zero_by_2070

Outputs
-------
Capacity outputs:
    pv_scenario_series_raw.csv
    wind_scenario_series_raw.csv
    pv_scenario_series_interpolated.csv
    wind_scenario_series_interpolated.csv
    pv_mean_by_group.csv
    wind_mean_by_group.csv
    pv_mean_by_group.png
    wind_mean_by_group.png

Cost/Wright-law outputs:
    pv_historical_cost_data_used.csv
    wind_historical_cost_data_used.csv
    pv_wright_fit_data.csv
    wind_wright_fit_data.csv
    pv_wright_learning_parameters.csv
    wind_wright_learning_parameters.csv
    pv_wright_cost_projection_by_group.csv
    wind_wright_cost_projection_by_group.csv
    pv_wright_cost_projection_to_2070.png
    pv_wright_cost_projection_to_2070_log.png
    wind_wright_cost_projection_to_2070.png
    wind_wright_cost_projection_to_2070_log.png
    pv_wright_experience_curve_fit.png
    wind_wright_experience_curve_fit.png

Run examples
------------
If all files are in the same folder:
    python analyse_pv_wind_wright_costs.py

Explicit workbook and cost files:
    python analyse_pv_wind_wright_costs.py --input SCI-2025_v1.0_pathways_ensemble_global.xlsx --historical-pv-cost-csv solar-pv-prices.csv --historical-wind-cost-csv costs-wind-over-time.csv

Manual learning rates, if you do not want to estimate them from the historical data:
    python analyse_pv_wind_wright_costs.py --manual-pv-learning-rate 0.20 --manual-wind-learning-rate 0.10
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NET_ZERO_COL = "Emissions Diagnostics|Year of Net Zero|CO2"
VETTING_COL = "Vetting|SCI 2025"
VETTING_OK_VALUE = "ok"

BY_2070 = "net_zero_by_2070"
NOT_BY_2070 = "not_net_zero_by_2070"

DEFAULT_PV_COST_FILE = "solar-pv-prices.csv"
DEFAULT_WIND_COST_FILE = "costs-wind-over-time.csv"

# Preferred variables found in the SCI workbook. The code chooses the first
# available option for each model-scenario to avoid double-counting aggregates
# and components.
TECH_VARIABLES = {
    "PV": {
        "capacity": [
            ["Capacity|Electricity|Solar|PV"],
            ["Capacity|Electricity|Solar|PV|Commercial", "Capacity|Electricity|Solar|PV|Residential"],
            ["Capacity|Electricity|Solar"],  # fallback: may include CSP if PV is unavailable
        ],
        "additions": [
            ["Capacity Additions|Electricity|Solar|PV"],
            [
                "Capacity Additions|Electricity|Solar|PV|Commercial",
                "Capacity Additions|Electricity|Solar|PV|Residential",
            ],
            ["Capacity Additions|Electricity|Solar"],  # fallback: may include CSP if PV is unavailable
        ],
    },
    "Wind": {
        "capacity": [
            ["Capacity|Electricity|Wind"],
            ["Capacity|Electricity|Wind|Onshore", "Capacity|Electricity|Wind|Offshore"],
        ],
        "additions": [
            ["Capacity Additions|Electricity|Wind"],
            ["Capacity Additions|Electricity|Wind|Onshore", "Capacity Additions|Electricity|Wind|Offshore"],
        ],
    },
}


# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names strings and strip accidental whitespace."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def all_needed_variables() -> set[str]:
    variables: set[str] = set()
    for spec in TECH_VARIABLES.values():
        for groups in spec.values():
            for variable_group in groups:
                variables.update(variable_group)
    return variables


# -----------------------------------------------------------------------------
# Fast XLSX reader for large IAMC sheets
# -----------------------------------------------------------------------------
# This avoids loading the whole Excel `data` sheet with pandas/openpyxl, which can
# be slow for this file. It streams the sheet XML and keeps only needed rows.

XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
OFFICE_REL_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _column_number(cell_reference: str) -> int:
    letters = "".join(ch for ch in cell_reference if ch.isalpha())
    number = 0
    for ch in letters.upper():
        number = number * 26 + ord(ch) - 64
    return number


def _load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except KeyError:
        return []

    strings: list[str] = []
    for si in root.findall(XLSX_NS + "si"):
        strings.append("".join(t.text or "" for t in si.iter(XLSX_NS + "t")))
    return strings


def _cell_value(cell: ET.Element, shared_strings: list[str]):
    cell_type = cell.attrib.get("t")
    v = cell.find(XLSX_NS + "v")

    if cell_type == "s":
        return shared_strings[int(v.text)] if v is not None and v.text is not None else None
    if cell_type == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(XLSX_NS + "t"))
    return v.text if v is not None else None


def _sheet_xml_path(zf: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall(REL_NS + "Relationship")}

    sheets = workbook.find(XLSX_NS + "sheets")
    if sheets is None:
        raise ValueError("Workbook has no sheets.")

    for sheet in sheets.findall(XLSX_NS + "sheet"):
        if sheet.attrib.get("name") == sheet_name:
            rel_id = sheet.attrib[OFFICE_REL_NS + "id"]
            target = rel_map[rel_id]
            return "xl/" + target.lstrip("/")

    raise ValueError(f"Sheet not found: {sheet_name}")


def xlsx_has_required_sheets(path: str | Path, required_sheets: set[str]) -> bool:
    """Return True if an xlsx file contains all required sheet names."""
    try:
        with zipfile.ZipFile(path) as zf:
            workbook = ET.fromstring(zf.read("xl/workbook.xml"))
            sheets = workbook.find(XLSX_NS + "sheets")
            if sheets is None:
                return False
            names = {sheet.attrib.get("name") for sheet in sheets.findall(XLSX_NS + "sheet")}
            return required_sheets.issubset(names)
    except Exception:
        return False


def read_xlsx_sheet_fast(
    path: str | Path,
    sheet_name: str,
    keep_variables: set[str] | None = None,
) -> pd.DataFrame:
    """Read an XLSX sheet into a DataFrame, optionally keeping only selected Variables."""
    rows: list[dict[str, object]] = []
    headers: dict[int, str] | None = None
    variable_col_number: int | None = None

    with zipfile.ZipFile(path) as zf:
        shared_strings = _load_shared_strings(zf)
        sheet_path = _sheet_xml_path(zf, sheet_name)

        with zf.open(sheet_path) as fh:
            for _, row_elem in ET.iterparse(fh, events=("end",)):
                if row_elem.tag != XLSX_NS + "row":
                    continue

                cells = row_elem.findall(XLSX_NS + "c")

                # Header row: parse every cell once to learn column names.
                if headers is None:
                    values_by_col: dict[int, object] = {}
                    for cell in cells:
                        col_number = _column_number(cell.attrib.get("r", ""))
                        values_by_col[col_number] = _cell_value(cell, shared_strings)

                    headers = {col: str(value).strip() for col, value in values_by_col.items() if value is not None}
                    variable_col_number = next(
                        (col for col, header in headers.items() if header.lower() == "variable"),
                        None,
                    )
                    row_elem.clear()
                    continue

                # Large-sheet optimization: if a variable filter is provided, read
                # only the Variable cell first. Most rows can then be skipped.
                if keep_variables is not None:
                    variable = None
                    for cell in cells:
                        if _column_number(cell.attrib.get("r", "")) == variable_col_number:
                            variable = _cell_value(cell, shared_strings)
                            break
                    if variable not in keep_variables:
                        row_elem.clear()
                        continue

                values_by_col = {}
                for cell in cells:
                    col_number = _column_number(cell.attrib.get("r", ""))
                    if col_number in headers:
                        values_by_col[col_number] = _cell_value(cell, shared_strings)

                rows.append({header: values_by_col.get(col) for col, header in headers.items()})
                row_elem.clear()

    return normalize_columns(pd.DataFrame(rows))


# -----------------------------------------------------------------------------
# Input handling
# -----------------------------------------------------------------------------


def find_default_workbook() -> Path | None:
    """Find the SCI workbook if the user did not pass --input."""
    script_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()
    search_dirs = [cwd]
    if script_dir != cwd:
        search_dirs.append(script_dir)

    preferred_name = "SCI-2025_v1.0_pathways_ensemble_global.xlsx"

    for folder in search_dirs:
        preferred = folder / preferred_name
        if preferred.exists() and xlsx_has_required_sheets(preferred, {"data", "meta"}):
            return preferred

    for folder in search_dirs:
        for candidate in sorted(folder.glob("*.xlsx")):
            if candidate.name.startswith("~$"):
                continue
            if xlsx_has_required_sheets(candidate, {"data", "meta"}):
                return candidate

    return None


def read_inputs(args: argparse.Namespace) -> tuple[pd.DataFrame, pd.DataFrame, Path | None]:
    needed = all_needed_variables()

    if args.data_csv and args.meta_csv:
        data = normalize_columns(pd.read_csv(args.data_csv))
        meta = normalize_columns(pd.read_csv(args.meta_csv))
        data = data[data["Variable"].isin(needed)].copy()
        return data, meta, None

    input_path: Path | None = Path(args.input) if args.input else find_default_workbook()
    if input_path is None:
        raise ValueError(
            "Provide either --input workbook.xlsx or both --data-csv and --meta-csv. "
            "Alternatively, place the SCI workbook in the same folder as the script."
        )

    data = read_xlsx_sheet_fast(input_path, "data", keep_variables=needed)
    meta = read_xlsx_sheet_fast(input_path, "meta")
    return data, meta, input_path


# -----------------------------------------------------------------------------
# Core capacity analysis
# -----------------------------------------------------------------------------


def year_columns(df: pd.DataFrame) -> list[str]:
    years = [str(c) for c in df.columns if re.fullmatch(r"\d{4}", str(c))]
    return sorted(years, key=int)


def prepare_numeric_years(df: pd.DataFrame, years: Iterable[str]) -> pd.DataFrame:
    df = df.copy()
    for year in years:
        df[year] = pd.to_numeric(df[year], errors="coerce")
    return df


def classify_scenarios(meta: pd.DataFrame) -> dict[tuple[str, str], str]:
    meta = meta.copy()
    if NET_ZERO_COL not in meta.columns:
        raise KeyError(f"Missing metadata column: {NET_ZERO_COL}")

    meta[NET_ZERO_COL] = pd.to_numeric(meta[NET_ZERO_COL], errors="coerce")
    meta["net_zero_group"] = np.where(meta[NET_ZERO_COL].le(2070), BY_2070, NOT_BY_2070)

    return {
        (str(row["Model"]), str(row["Scenario"])): row["net_zero_group"]
        for _, row in meta.iterrows()
    }



def filter_to_vetted_scenarios(
    data: pd.DataFrame,
    meta: pd.DataFrame,
    use_vetted_only: bool = True,
    vetting_col: str = VETTING_COL,
    ok_value: str = VETTING_OK_VALUE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Keep only scenarios whose SCI 2025 vetting status is "ok".

    The vetting column is expected in the meta sheet. Filtering is done by the
    joint key (Model, Scenario), then applied to both meta and data.

    Returns:
        data_filtered, meta_filtered, summary_table, scenario_list
    """
    required_cols = {"Model", "Scenario"}
    missing_meta_cols = required_cols - set(meta.columns)
    missing_data_cols = required_cols - set(data.columns)
    if missing_meta_cols:
        raise KeyError(f"The meta sheet is missing columns: {sorted(missing_meta_cols)}")
    if missing_data_cols:
        raise KeyError(f"The data sheet is missing columns: {sorted(missing_data_cols)}")

    meta = meta.copy()
    data = data.copy()

    total_meta_scenarios = meta[["Model", "Scenario"]].drop_duplicates().shape[0]
    total_data_scenarios = data[["Model", "Scenario"]].drop_duplicates().shape[0]

    if not use_vetted_only:
        scenario_list_cols = ["Model", "Scenario"]
        if vetting_col in meta.columns:
            scenario_list_cols.append(vetting_col)
        if NET_ZERO_COL in meta.columns:
            scenario_list_cols.append(NET_ZERO_COL)

        scenario_list = meta[scenario_list_cols].drop_duplicates().copy()
        summary = pd.DataFrame(
            [
                {
                    "use_vetted_only": False,
                    "vetting_column": vetting_col,
                    "ok_value": ok_value,
                    "meta_scenarios_before_filter": total_meta_scenarios,
                    "meta_scenarios_after_filter": total_meta_scenarios,
                    "data_scenarios_before_filter": total_data_scenarios,
                    "data_scenarios_after_filter": total_data_scenarios,
                    "data_rows_before_filter": len(data),
                    "data_rows_after_filter": len(data),
                }
            ]
        )
        return data, meta, summary, scenario_list

    if vetting_col not in meta.columns:
        raise KeyError(
            f"Missing metadata column: {vetting_col}. "
            "Cannot filter to SCI-vetted scenarios. Use --no-use-vetted-only to disable this filter."
        )

    vetting_normalized = meta[vetting_col].astype(str).str.strip().str.lower()
    meta_filtered = meta[vetting_normalized.eq(str(ok_value).strip().lower())].copy()

    keep_pairs = set(
        zip(
            meta_filtered["Model"].astype(str),
            meta_filtered["Scenario"].astype(str),
        )
    )

    data_mask = data[["Model", "Scenario"]].astype(str).apply(
        lambda row: (row["Model"], row["Scenario"]) in keep_pairs,
        axis=1,
    )
    data_filtered = data[data_mask].copy()

    scenario_list_cols = ["Model", "Scenario", vetting_col]
    if NET_ZERO_COL in meta_filtered.columns:
        scenario_list_cols.append(NET_ZERO_COL)
    scenario_list = meta_filtered[scenario_list_cols].drop_duplicates().copy()

    summary = pd.DataFrame(
        [
            {
                "use_vetted_only": True,
                "vetting_column": vetting_col,
                "ok_value": ok_value,
                "meta_scenarios_before_filter": total_meta_scenarios,
                "meta_scenarios_after_filter": meta_filtered[["Model", "Scenario"]].drop_duplicates().shape[0],
                "data_scenarios_before_filter": total_data_scenarios,
                "data_scenarios_after_filter": data_filtered[["Model", "Scenario"]].drop_duplicates().shape[0],
                "data_rows_before_filter": len(data),
                "data_rows_after_filter": len(data_filtered),
            }
        ]
    )

    if data_filtered.empty:
        raise ValueError(
            f"After filtering to {vetting_col} == {ok_value!r}, no PV/wind-relevant data rows remain."
        )

    return data_filtered, meta_filtered, summary, scenario_list


def _sum_available_variables(
    scenario_df: pd.DataFrame,
    variables: list[str],
    years: list[str],
) -> tuple[pd.Series | None, list[str]]:
    available = [v for v in variables if v in set(scenario_df["Variable"])]
    if not available:
        return None, []

    subset = scenario_df[scenario_df["Variable"].isin(available)]
    series = subset[years].sum(axis=0, min_count=1)
    series.index = [int(y) for y in years]
    return series.astype(float), available


def additions_to_cumulative_gw(additions_gw_per_year: pd.Series) -> pd.Series:
    """
    Convert GW/yr to cumulative GW using the model time step.

    The first model year is set to zero cumulative additions. Every later point
    is approximated as annual additions multiplied by the years since the
    previous reported model year.
    """
    additions = additions_gw_per_year.sort_index().astype(float)
    years = pd.Series(additions.index, index=additions.index, dtype=float)
    interval_lengths = years.diff().fillna(0.0)
    return (additions * interval_lengths).cumsum()


def extract_cumulative_capacity(
    scenario_df: pd.DataFrame,
    tech: str,
    years: list[str],
) -> tuple[pd.Series | None, str, list[str]]:
    spec = TECH_VARIABLES[tech]

    # Prefer direct installed capacity in GW.
    for variables in spec["capacity"]:
        series, used = _sum_available_variables(scenario_df, variables, years)
        if series is not None:
            return series, "reported_capacity_GW", used

    # Fallback: integrate capacity additions in GW/yr to cumulative GW.
    for variables in spec["additions"]:
        additions, used = _sum_available_variables(scenario_df, variables, years)
        if additions is not None:
            return additions_to_cumulative_gw(additions), "integrated_additions_GW", used

    return None, "missing", []


def build_dictionary_and_records(
    data: pd.DataFrame,
    classification: dict[tuple[str, str], str],
    tech: str,
    years: list[str],
) -> tuple[dict[str, dict[str, pd.Series]], pd.DataFrame, pd.DataFrame]:
    technology_dictionary: dict[str, dict[str, pd.Series]] = {BY_2070: {}, NOT_BY_2070: {}}
    long_records: list[dict[str, object]] = []
    missing_records: list[dict[str, object]] = []

    for (model, scenario), scenario_df in data.groupby(["Model", "Scenario"], sort=False):
        key = (str(model), str(scenario))
        group = classification.get(key, NOT_BY_2070)
        series, source_method, variables_used = extract_cumulative_capacity(scenario_df, tech, years)
        scenario_name = f"{model} | {scenario}"

        if series is None:
            missing_records.append({"Model": model, "Scenario": scenario, "technology": tech})
            continue

        technology_dictionary[group][scenario_name] = series
        for year, value in series.items():
            long_records.append(
                {
                    "Model": model,
                    "Scenario": scenario,
                    "scenario_name": scenario_name,
                    "group": group,
                    "technology": tech,
                    "year": int(year),
                    "value_GW": value,
                    "source_method": source_method,
                    "variables_used": "; ".join(variables_used),
                }
            )

    return technology_dictionary, pd.DataFrame(long_records), pd.DataFrame(missing_records)


# -----------------------------------------------------------------------------
# Interpolation and optional monotonic correction
# -----------------------------------------------------------------------------


def interpolate_each_scenario(
    records: pd.DataFrame,
    target_years: list[int],
    interpolate_missing_years: bool = True,
    enforce_monotonic: bool = False,
    min_valid_points: int = 2,
) -> pd.DataFrame:
    """
    Fill missing internal years within each Model-Scenario trajectory.

    This addresses the saw-tooth group mean that appears when many scenarios
    report only decadal years but a smaller subset reports intermediate years.
    The interpolation is performed before averaging, so group means are based on
    a more consistent sample composition.

    The function does not extrapolate before the first reported value or after
    the last reported value.
    """
    if records.empty:
        return records.copy()

    group_cols = [
        "Model",
        "Scenario",
        "scenario_name",
        "group",
        "technology",
        "source_method",
        "variables_used",
    ]

    filled_records: list[dict[str, object]] = []
    target_years = sorted(int(y) for y in target_years)

    for keys, df in records.groupby(group_cols, dropna=False, sort=False):
        df = df.sort_values("year")
        raw_series = df.groupby("year")["value_GW"].mean().astype(float)
        raw_series = raw_series.reindex(target_years)

        series = raw_series.copy()

        if interpolate_missing_years and raw_series.notna().sum() >= min_valid_points:
            series = series.interpolate(method="linear", limit_area="inside")

        if enforce_monotonic:
            # Use only if you want to interpret the quantity as cumulative ever-built
            # capacity. Reported installed capacity stocks can in principle decline.
            series = series.cummax()

        info = dict(zip(group_cols, keys))

        for year in target_years:
            raw_value = raw_series.loc[year]
            value = series.loc[year]
            filled_records.append(
                {
                    **info,
                    "year": int(year),
                    "value_GW": value,
                    "raw_value_GW": raw_value,
                    "is_interpolated": bool(pd.isna(raw_value) and pd.notna(value)),
                }
            )

    return pd.DataFrame(filled_records)


def records_to_dictionary(records: pd.DataFrame) -> dict[str, dict[str, pd.Series]]:
    """Convert long scenario records back into the dictionary requested in the task."""
    technology_dictionary: dict[str, dict[str, pd.Series]] = {BY_2070: {}, NOT_BY_2070: {}}

    if records.empty:
        return technology_dictionary

    for (group, scenario_name), df in records.groupby(["group", "scenario_name"], sort=False):
        series = df.sort_values("year").set_index("year")["value_GW"].astype(float)
        technology_dictionary.setdefault(str(group), {})[str(scenario_name)] = series

    return technology_dictionary


def mean_series_from_records(records: pd.DataFrame) -> pd.DataFrame:
    """Mean trajectory by net-zero group from long records."""
    if records.empty:
        return pd.DataFrame()

    mean_df = (
        records.dropna(subset=["value_GW"])
        .groupby(["year", "group"])["value_GW"]
        .mean()
        .unstack("group")
        .sort_index()
    )
    mean_df.index.name = "year"
    return mean_df


def scenario_counts_by_year(records: pd.DataFrame) -> pd.DataFrame:
    """Count how many model-scenarios contribute to each group-year mean."""
    if records.empty:
        return pd.DataFrame(columns=["technology", "group", "year", "n_scenarios"])

    return (
        records.dropna(subset=["value_GW"])
        .groupby(["technology", "group", "year"])["scenario_name"]
        .nunique()
        .reset_index(name="n_scenarios")
        .sort_values(["technology", "group", "year"])
    )



# -----------------------------------------------------------------------------
# Wright-law PV and wind cost analysis
# -----------------------------------------------------------------------------


def normalize_name(name: str) -> str:
    """Normalize column names for flexible matching."""
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")


def find_column(df: pd.DataFrame, names: list[str]) -> str | None:
    """Find a column by exact name or normalized lowercase name."""
    exact = {str(c): str(c) for c in df.columns}
    normalized = {normalize_name(str(c)): str(c) for c in df.columns}

    for name in names:
        if name in exact:
            return exact[name]
        key = normalize_name(name)
        if key in normalized:
            return normalized[key]
    return None


def read_csv_flexible(path: str | Path) -> pd.DataFrame:
    """
    Read CSV files with either comma or semicolon delimiters.

    Your uploaded files are semicolon-separated. This function also drops the
    empty trailing columns that appear in the wind-cost file.
    """
    df = pd.read_csv(path, sep=None, engine="python")
    df = normalize_columns(df)
    df = df.dropna(axis=1, how="all")
    return df


def find_default_cost_file(filename: str) -> Path | None:
    """Find a local cost file in the current working directory or script folder."""
    script_dir = Path(__file__).resolve().parent
    cwd = Path.cwd().resolve()
    search_dirs = [cwd]
    if script_dir != cwd:
        search_dirs.append(script_dir)

    for folder in search_dirs:
        candidate = folder / filename
        if candidate.exists():
            return candidate
    return None


def standardize_cost_unit_to_usd_per_kw(
    cost_values: pd.Series,
    technology: str,
    input_unit: str = "auto",
) -> tuple[pd.Series, str, float]:
    """
    Convert costs to USD/kW.

    input_unit options:
        - auto: infer from magnitude
        - usd_per_w: multiply by 1000
        - usd_per_kw: keep unchanged

    The solar OWID file often reports USD/W, e.g. 0.26 USD/W in 2024. The
    output required for this analysis is USD/kW, so automatic detection converts
    such values to about 260 USD/kW.
    """
    values = pd.to_numeric(cost_values, errors="coerce")

    if input_unit not in {"auto", "usd_per_w", "usd_per_kw"}:
        raise ValueError("input_unit must be one of: auto, usd_per_w, usd_per_kw")

    if input_unit == "usd_per_w":
        return values * 1000.0, "usd_per_w_converted_to_usd_per_kw", 1000.0

    if input_unit == "usd_per_kw":
        return values, "usd_per_kw", 1.0

    # Auto-detection heuristic. Costs below about 20 are almost certainly USD/W
    # for energy technologies; costs in USD/kW are usually hundreds or thousands.
    median_value = float(values.dropna().median()) if values.dropna().size else np.nan
    if np.isfinite(median_value) and median_value < 20.0:
        return values * 1000.0, "auto_detected_usd_per_w_converted_to_usd_per_kw", 1000.0

    return values, "auto_detected_usd_per_kw", 1.0


def read_historical_cost_data(
    path: str | Path | None,
    technology: str,
    default_filename: str,
    input_unit: str = "auto",
) -> tuple[pd.DataFrame | None, str]:
    """
    Read a historical technology-cost time series and standardize it to USD/kW.

    Standardized output columns:
        year, cost_usd_per_kw, raw_cost_value, assumed_input_unit, unit_factor_to_usd_per_kw
    """
    if path is None:
        found = find_default_cost_file(default_filename)
        if found is None:
            return None, "not_available"
        path = found

    raw = read_csv_flexible(path)

    # Keep World for the solar file if available. Keep all rows for wind unless
    # there are multiple entities; then retain rows mentioning wind.
    if "Entity" in raw.columns:
        entity_lower = raw["Entity"].astype(str).str.lower()
        if technology.upper() == "PV" and entity_lower.eq("world").any():
            raw = raw[entity_lower.eq("world")].copy()
        elif technology.upper() == "WIND" and entity_lower.str.contains("wind", na=False).any():
            raw = raw[entity_lower.str.contains("wind", na=False)].copy()

    year_col = find_column(raw, ["year", "Year"])

    if technology.upper() == "PV":
        cost_col = find_column(
            raw,
            [
                "cost_usd_per_kw",
                "cost_usd_per_w",
                "Solar PV module cost",
                "solar_pv_module_cost",
                "PV module cost",
                "Technology cost",
                "cost",
            ],
        )
    else:
        cost_col = find_column(
            raw,
            [
                "cost_usd_per_kw",
                "Technology cost",
                "Wind turbine cost",
                "wind_turbine_cost",
                "cost",
            ],
        )

    if year_col is None or cost_col is None:
        raise ValueError(
            f"Could not identify year/cost columns in {path}. Found columns: {list(raw.columns)}"
        )

    cost_usd_per_kw, assumed_unit, factor = standardize_cost_unit_to_usd_per_kw(
        raw[cost_col],
        technology=technology,
        input_unit=input_unit,
    )

    out = pd.DataFrame(
        {
            "year": pd.to_numeric(raw[year_col], errors="coerce"),
            "cost_usd_per_kw": cost_usd_per_kw,
            "raw_cost_value": pd.to_numeric(raw[cost_col], errors="coerce"),
            "assumed_input_unit": assumed_unit,
            "unit_factor_to_usd_per_kw": factor,
            "technology": technology,
        }
    )

    out = out.dropna(subset=["year", "cost_usd_per_kw"])
    out = out[out["cost_usd_per_kw"] > 0]
    out["year"] = out["year"].astype(int)
    out = out.sort_values("year").drop_duplicates("year", keep="last").reset_index(drop=True)

    if out.empty:
        raise ValueError(f"Historical {technology} cost data was read, but no valid positive rows were found.")

    return out, str(path)


def interpolate_historical_cost_to_years(historical: pd.DataFrame, years: list[int]) -> pd.Series:
    """Interpolate historical costs to selected years, without extrapolation."""
    hist = historical.sort_values("year")
    x = hist["year"].to_numpy(dtype=float)
    y = hist["cost_usd_per_kw"].to_numpy(dtype=float)

    result = {}
    for year in years:
        year_float = float(year)
        if year_float < x.min() or year_float > x.max():
            result[int(year)] = np.nan
        else:
            result[int(year)] = float(np.interp(year_float, x, y))
    return pd.Series(result, name="cost_usd_per_kw")


def prepare_wright_fit_data(
    historical: pd.DataFrame,
    mean_capacity: pd.DataFrame,
    technology: str,
    fit_start_year: int | None = None,
    fit_end_year: int | None = None,
) -> pd.DataFrame:
    """
    Build the dataset used to estimate Wright's law.

    Historical cost is matched to the average of the two scenario-group capacity
    trajectories over overlapping years. The resulting fit is deliberately simple
    and transparent for the summer-school exercise.
    """
    if mean_capacity.empty:
        raise ValueError(f"{technology} mean capacity trajectory is empty; cannot estimate Wright's law.")

    capacity = mean_capacity.copy().sort_index()
    capacity.index = [int(y) for y in capacity.index]
    capacity_average = capacity.mean(axis=1, skipna=True)

    candidate_years = sorted(set(int(y) for y in capacity_average.index))
    candidate_years = [y for y in candidate_years if y >= int(historical["year"].min())]
    candidate_years = [y for y in candidate_years if y <= int(historical["year"].max())]

    if fit_start_year is not None:
        candidate_years = [y for y in candidate_years if y >= fit_start_year]
    if fit_end_year is not None:
        candidate_years = [y for y in candidate_years if y <= fit_end_year]

    cost_at_years = interpolate_historical_cost_to_years(historical, candidate_years)

    records = []
    for year in candidate_years:
        cap = float(capacity_average.loc[year]) if year in capacity_average.index else np.nan
        cost = float(cost_at_years.loc[year]) if year in cost_at_years.index else np.nan
        if np.isfinite(cap) and np.isfinite(cost) and cap > 0 and cost > 0:
            records.append(
                {
                    "technology": technology,
                    "year": int(year),
                    "capacity_gw": cap,
                    "cost_usd_per_kw": cost,
                }
            )

    fit_data = pd.DataFrame(records)
    if len(fit_data) < 3:
        raise ValueError(
            f"Need at least 3 overlapping historical cost / SCI capacity points to fit Wright's law for {technology}. "
            f"Found {len(fit_data)}. Use --manual-pv-learning-rate or --manual-wind-learning-rate if needed."
        )

    return fit_data


def estimate_wright_learning_from_fit_data(
    fit_data: pd.DataFrame,
    historical: pd.DataFrame,
    technology: str,
) -> dict[str, float | int | str]:
    """
    Estimate Wright's law:

        log(cost) = intercept - b * log(cumulative capacity)
    """
    df = fit_data.dropna(subset=["cost_usd_per_kw", "capacity_gw"]).copy()
    df = df[(df["cost_usd_per_kw"] > 0) & (df["capacity_gw"] > 0)]

    if len(df) < 3:
        raise ValueError(f"Need at least 3 observations to fit Wright's law for {technology}.")

    x = np.log(df["capacity_gw"].to_numpy(dtype=float))
    y = np.log(df["cost_usd_per_kw"].to_numpy(dtype=float))

    slope, intercept = np.polyfit(x, y, deg=1)
    b = -float(slope)
    progress_ratio = 2.0 ** (-b)
    learning_rate = 1.0 - progress_ratio

    y_hat = intercept + slope * x
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

    latest = historical.loc[historical["year"].idxmax()]

    return {
        "technology": technology,
        "method": "historical_cost_vs_sci_capacity_log_log_fit",
        "fit_start_year": int(df["year"].min()),
        "fit_end_year": int(df["year"].max()),
        "n_observations": int(len(df)),
        "intercept": float(intercept),
        "slope": float(slope),
        "wright_exponent_b": float(b),
        "progress_ratio": float(progress_ratio),
        "learning_rate": float(learning_rate),
        "r_squared_log_log": float(r2),
        "latest_historical_year": int(latest["year"]),
        "latest_historical_cost_usd_per_kw": float(latest["cost_usd_per_kw"]),
    }


def manual_wright_parameters(
    historical: pd.DataFrame | None,
    technology: str,
    learning_rate: float,
    base_cost_usd_per_kw: float | None,
) -> dict[str, float | int | str]:
    """Create Wright-law parameters from a user-provided learning rate."""
    if not (0 < learning_rate < 1):
        raise ValueError("Manual learning rate must be between 0 and 1, e.g. 0.20 for 20%.")

    b = -np.log2(1.0 - learning_rate)
    progress_ratio = 1.0 - learning_rate

    if historical is not None and not historical.empty:
        latest = historical.loc[historical["year"].idxmax()]
        latest_year = int(latest["year"])
        latest_cost = float(latest["cost_usd_per_kw"])
    else:
        latest_year = 2024
        latest_cost = np.nan

    if base_cost_usd_per_kw is not None:
        latest_cost = float(base_cost_usd_per_kw)

    if not np.isfinite(latest_cost) or latest_cost <= 0:
        raise ValueError(
            f"Manual learning was requested for {technology}, but no valid base cost is available. "
            f"Pass --base-{technology.lower()}-cost-usd-per-kw or provide historical cost data."
        )

    return {
        "technology": technology,
        "method": "manual_learning_rate",
        "fit_start_year": np.nan,
        "fit_end_year": np.nan,
        "n_observations": 0 if historical is None else int(len(historical)),
        "intercept": np.nan,
        "slope": -float(b),
        "wright_exponent_b": float(b),
        "progress_ratio": float(progress_ratio),
        "learning_rate": float(learning_rate),
        "r_squared_log_log": np.nan,
        "latest_historical_year": int(latest_year),
        "latest_historical_cost_usd_per_kw": float(latest_cost),
    }


def estimate_cost_projection_by_group(
    mean_capacity: pd.DataFrame,
    params: dict[str, float | int | str],
    technology: str,
    target_end_year: int = 2070,
    anchor_year: int | None = None,
) -> pd.DataFrame:
    """
    Estimate technology costs by group using Wright's law.

    Projection is anchored to the latest historical cost:
        cost_g,t = cost_anchor * (capacity_g,t / capacity_g,anchor) ** (-b)
    """
    if mean_capacity.empty:
        raise ValueError(f"{technology} mean trajectory is empty; cannot estimate costs.")

    capacity = mean_capacity.copy().sort_index()
    capacity.index = [int(y) for y in capacity.index]
    capacity = capacity[capacity.index <= int(target_end_year)]

    if capacity.empty:
        raise ValueError(f"No {technology} scenario years are available up to {target_end_year}.")

    latest_hist_year = int(params["latest_historical_year"])
    cost_anchor = float(params["latest_historical_cost_usd_per_kw"])
    b = float(params["wright_exponent_b"])

    if not np.isfinite(cost_anchor) or cost_anchor <= 0:
        raise ValueError(f"Invalid anchor cost for {technology}.")

    available_years = [int(y) for y in capacity.index]
    if anchor_year is None:
        future_years = [y for y in available_years if y >= latest_hist_year]
        if not future_years:
            future_years = available_years
        anchor_year = min(future_years)
    else:
        anchor_year = int(anchor_year)
        if anchor_year not in available_years:
            raise ValueError(f"Requested anchor year {anchor_year} is not in {technology} scenario years.")

    records: list[dict[str, object]] = []
    tech_lower = technology.lower()

    for group in capacity.columns:
        group_series = pd.to_numeric(capacity[group], errors="coerce").dropna()
        group_series = group_series[(group_series.index <= target_end_year) & (group_series > 0)]

        if anchor_year not in group_series.index:
            print(f"WARNING: group {group} has no positive {technology} capacity in anchor year {anchor_year}; skipped.")
            continue

        anchor_capacity = float(group_series.loc[anchor_year])
        if not np.isfinite(anchor_capacity) or anchor_capacity <= 0:
            print(f"WARNING: group {group} has invalid {technology} capacity in anchor year {anchor_year}; skipped.")
            continue

        for year, capacity_gw in group_series.items():
            year = int(year)
            if year < anchor_year or year > target_end_year:
                continue

            relative_experience = float(capacity_gw) / anchor_capacity
            cost = cost_anchor * relative_experience ** (-b)

            records.append(
                {
                    "technology": technology,
                    "group": group,
                    "year": year,
                    f"{tech_lower}_capacity_gw": float(capacity_gw),
                    "anchor_year": int(anchor_year),
                    "anchor_capacity_gw": float(anchor_capacity),
                    "anchor_cost_usd_per_kw": float(cost_anchor),
                    "relative_experience_vs_anchor": float(relative_experience),
                    "wright_exponent_b": float(b),
                    "learning_rate": float(params["learning_rate"]),
                    "cost_usd_per_kw": float(cost),
                }
            )

    if not records:
        raise ValueError(f"No {technology} cost projection records were created.")

    return pd.DataFrame(records).sort_values(["technology", "group", "year"]).reset_index(drop=True)
# -----------------------------------------------------------------------------
# Plotting and reporting
# -----------------------------------------------------------------------------


def plot_mean(mean_df: pd.DataFrame, title: str, output_path: Path) -> None:
    plt.figure(figsize=(9, 5))
    for group in mean_df.columns:
        plt.plot(mean_df.index, mean_df[group], marker="o", label=group)

    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Mean cumulative capacity / installation (GW)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_counts(counts: pd.DataFrame, tech: str, output_path: Path) -> None:
    tech_counts = counts[counts["technology"] == tech]
    if tech_counts.empty:
        return

    pivot = tech_counts.pivot(index="year", columns="group", values="n_scenarios").sort_index()

    plt.figure(figsize=(9, 4))
    for group in pivot.columns:
        plt.plot(pivot.index, pivot[group], marker="o", label=group)

    plt.title(f"{tech} number of scenarios contributing to each year")
    plt.xlabel("Year")
    plt.ylabel("Number of scenarios")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()



def plot_cost_projection(
    technology: str,
    historical: pd.DataFrame | None,
    projection: pd.DataFrame,
    output_path: Path,
    target_end_year: int,
    log_y: bool = False,
) -> None:
    """Plot historical technology cost and Wright-law projections."""
    plt.figure(figsize=(10, 5.5))

    if historical is not None and not historical.empty:
        hist = historical[historical["year"] <= target_end_year].copy()
        plt.plot(
            hist["year"],
            hist["cost_usd_per_kw"],
            marker="o",
            linewidth=2,
            label=f"Historical {technology} cost",
            color="black",
        )

    for group, df in projection.groupby("group", sort=False):
        plt.plot(
            df["year"],
            df["cost_usd_per_kw"],
            marker="o",
            linewidth=2,
            label=f"Wright projection - {group}",
        )

    title_suffix = " - log scale" if log_y else ""
    plt.title(f"{technology} cost projection using Wright's law to {target_end_year}{title_suffix}")
    plt.xlabel("Year")
    plt.ylabel(f"{technology} cost (USD/kW)")
    if log_y:
        plt.yscale("log")
    plt.grid(True, alpha=0.3, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_wright_experience_curve_fit(
    technology: str,
    fit_data: pd.DataFrame | None,
    params: dict[str, float | int | str],
    output_path: Path,
) -> None:
    """Plot the fitted Wright curve in log-log space."""
    if fit_data is None or fit_data.empty:
        return
    if str(params.get("method")) == "manual_learning_rate":
        return

    df = fit_data.copy()
    df = df[(df["cost_usd_per_kw"] > 0) & (df["capacity_gw"] > 0)]
    if df.empty:
        return

    intercept = float(params["intercept"])
    slope = float(params["slope"])

    x_min = df["capacity_gw"].min()
    x_max = df["capacity_gw"].max()
    x_fit = np.exp(np.linspace(np.log(x_min), np.log(x_max), 200))
    y_fit = np.exp(intercept + slope * np.log(x_fit))

    plt.figure(figsize=(7, 5.5))
    plt.scatter(df["capacity_gw"], df["cost_usd_per_kw"], label="Fit data")
    plt.plot(x_fit, y_fit, label="Fitted Wright curve")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(f"Mean installed {technology} capacity (GW, log scale)")
    plt.ylabel(f"{technology} cost (USD/kW, log scale)")
    plt.title(f"{technology} historical experience curve fit")
    plt.grid(True, alpha=0.3, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def save_outputs_for_technology(
    outdir: Path,
    tech_lower: str,
    records_raw: pd.DataFrame,
    records_final: pd.DataFrame,
    missing: pd.DataFrame,
    mean_raw: pd.DataFrame,
    mean_final: pd.DataFrame,
) -> None:
    records_raw.to_csv(outdir / f"{tech_lower}_scenario_series_raw.csv", index=False)
    records_final.to_csv(outdir / f"{tech_lower}_scenario_series_interpolated.csv", index=False)
    missing.to_csv(outdir / f"{tech_lower}_missing_scenarios.csv", index=False)
    mean_raw.to_csv(outdir / f"{tech_lower}_mean_by_group_raw.csv")
    mean_final.to_csv(outdir / f"{tech_lower}_mean_by_group.csv")


# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Path to workbook with sheets named data and meta")
    parser.add_argument("--data-csv", help="Optional CSV export of the data sheet")
    parser.add_argument("--meta-csv", help="Optional CSV export of the meta sheet")
    parser.add_argument("--outdir", default="results", help="Output folder")
    parser.add_argument(
        "--use-vetted-only",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Keep only scenarios with Vetting|SCI 2025 == 'ok' before computing capacity "
            "and cost results. Default: true. Use --no-use-vetted-only to analyse all scenarios."
        ),
    )
    parser.add_argument(
        "--interpolate-missing-years",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Interpolate missing internal years within each scenario before averaging. Default: true.",
    )
    parser.add_argument(
        "--enforce-monotonic",
        action="store_true",
        help="Apply cumulative maximum within each scenario after interpolation. Optional; not used by default.",
    )
    parser.add_argument(
        "--min-valid-points",
        type=int,
        default=2,
        help="Minimum non-missing points required to interpolate a scenario. Default: 2.",
    )

    # Wright-law / cost options.
    parser.add_argument(
        "--estimate-costs",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Estimate PV and wind costs using Wright's law. Default: true.",
    )
    parser.add_argument(
        "--historical-pv-cost-csv",
        help="Optional local CSV with historical solar/PV costs. Default: solar-pv-prices.csv if found.",
    )
    parser.add_argument(
        "--historical-wind-cost-csv",
        help="Optional local CSV with historical wind costs. Default: costs-wind-over-time.csv if found.",
    )
    parser.add_argument(
        "--pv-cost-input-unit",
        choices=["auto", "usd_per_w", "usd_per_kw"],
        default="auto",
        help="Unit of the PV historical cost column. Default: auto.",
    )
    parser.add_argument(
        "--wind-cost-input-unit",
        choices=["auto", "usd_per_w", "usd_per_kw"],
        default="auto",
        help="Unit of the wind historical cost column. Default: auto.",
    )
    parser.add_argument(
        "--manual-pv-learning-rate",
        type=float,
        help="Optional manual PV learning rate, e.g. 0.20 for 20 percent. Overrides fitted PV learning.",
    )
    parser.add_argument(
        "--manual-wind-learning-rate",
        type=float,
        help="Optional manual wind learning rate, e.g. 0.10 for 10 percent. Overrides fitted wind learning.",
    )
    parser.add_argument(
        "--base-pv-cost-usd-per-kw",
        type=float,
        help="Base PV cost in USD/kW used with --manual-pv-learning-rate if no historical PV cost data is available.",
    )
    parser.add_argument(
        "--base-wind-cost-usd-per-kw",
        type=float,
        help="Base wind cost in USD/kW used with --manual-wind-learning-rate if no historical wind cost data is available.",
    )
    parser.add_argument(
        "--wright-fit-start-year",
        type=int,
        default=None,
        help="Optional first historical year for Wright-law log-log fit.",
    )
    parser.add_argument(
        "--wright-fit-end-year",
        type=int,
        default=None,
        help="Optional last historical year for Wright-law log-log fit.",
    )
    parser.add_argument(
        "--pv-cost-anchor-year",
        type=int,
        default=None,
        help="Optional model year where future PV cost projections are anchored. Default: first scenario year >= latest historical year.",
    )
    parser.add_argument(
        "--wind-cost-anchor-year",
        type=int,
        default=None,
        help="Optional model year where future wind cost projections are anchored. Default: first scenario year >= latest historical year.",
    )
    parser.add_argument(
        "--cost-end-year",
        type=int,
        default=2070,
        help="Last year shown in cost projections. Default: 2070.",
    )

    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    data, meta, workbook_path = read_inputs(args)
    years = year_columns(data)
    years_int = [int(y) for y in years]

    if not years:
        raise ValueError("No year columns were found in the data sheet.")

    data = prepare_numeric_years(data, years)

    # Keep only the SCI-vetted scenarios, unless disabled by --no-use-vetted-only.
    data, meta, vetting_summary, vetted_scenarios = filter_to_vetted_scenarios(
        data=data,
        meta=meta,
        use_vetted_only=args.use_vetted_only,
    )
    vetting_summary.to_csv(outdir / "00_vetting_filter_summary.csv", index=False)
    vetted_scenarios.to_csv(outdir / "00_vetted_scenarios_used.csv", index=False)

    classification = classify_scenarios(meta)

    scenario_groups = data.groupby(["Model", "Scenario"], sort=False)
    print(f"Loaded {len(scenario_groups)} model-scenario groups with PV/wind-relevant rows.")
    if workbook_path is not None:
        print(f"Input workbook: {workbook_path}")
    print(f"Years used: {min(years_int)}-{max(years_int)}")
    print(f"Use only SCI-vetted scenarios: {args.use_vetted_only}")
    print("Vetting filter summary:")
    print(vetting_summary.T.to_string(header=False))
    print(f"Interpolate missing internal years: {args.interpolate_missing_years}")
    print(f"Enforce monotonic trajectories: {args.enforce_monotonic}")

    # Raw extraction from the workbook.
    pv_dictionary_raw, pv_records_raw, pv_missing = build_dictionary_and_records(data, classification, "PV", years)
    wind_dictionary_raw, wind_records_raw, wind_missing = build_dictionary_and_records(data, classification, "Wind", years)

    # Raw means are saved for diagnostics. These are the ones that can show saw-tooth
    # behaviour when the sample changes across years.
    pv_mean_raw = mean_series_from_records(pv_records_raw)
    wind_mean_raw = mean_series_from_records(wind_records_raw)

    # Improved records: interpolate within each scenario before averaging.
    pv_records_final = interpolate_each_scenario(
        pv_records_raw,
        target_years=years_int,
        interpolate_missing_years=args.interpolate_missing_years,
        enforce_monotonic=args.enforce_monotonic,
        min_valid_points=args.min_valid_points,
    )
    wind_records_final = interpolate_each_scenario(
        wind_records_raw,
        target_years=years_int,
        interpolate_missing_years=args.interpolate_missing_years,
        enforce_monotonic=args.enforce_monotonic,
        min_valid_points=args.min_valid_points,
    )

    # These are the final dictionaries requested in the original task.
    pv_dictionary = records_to_dictionary(pv_records_final)
    wind_dictionary = records_to_dictionary(wind_records_final)

    # Final means used in the main plots.
    pv_mean = mean_series_from_records(pv_records_final)
    wind_mean = mean_series_from_records(wind_records_final)

    # Counts: useful to check whether sample-size changes are driving the plot.
    pv_counts_raw = scenario_counts_by_year(pv_records_raw)
    wind_counts_raw = scenario_counts_by_year(wind_records_raw)
    pv_counts_final = scenario_counts_by_year(pv_records_final)
    wind_counts_final = scenario_counts_by_year(wind_records_final)

    pv_counts_raw.to_csv(outdir / "pv_scenario_counts_by_year_raw.csv", index=False)
    wind_counts_raw.to_csv(outdir / "wind_scenario_counts_by_year_raw.csv", index=False)
    pv_counts_final.to_csv(outdir / "pv_scenario_counts_by_year_interpolated.csv", index=False)
    wind_counts_final.to_csv(outdir / "wind_scenario_counts_by_year_interpolated.csv", index=False)

    save_outputs_for_technology(outdir, "pv", pv_records_raw, pv_records_final, pv_missing, pv_mean_raw, pv_mean)
    save_outputs_for_technology(outdir, "wind", wind_records_raw, wind_records_final, wind_missing, wind_mean_raw, wind_mean)

    # Main improved plots.
    plot_mean(pv_mean, "PV mean cumulative capacity by net-zero group", outdir / "pv_mean_by_group.png")
    plot_mean(wind_mean, "Wind mean cumulative capacity by net-zero group", outdir / "wind_mean_by_group.png")

    # Raw plots for comparison and debugging.
    plot_mean(pv_mean_raw, "PV mean cumulative capacity by net-zero group - raw", outdir / "pv_mean_by_group_raw.png")
    plot_mean(wind_mean_raw, "Wind mean cumulative capacity by net-zero group - raw", outdir / "wind_mean_by_group_raw.png")

    # Scenario-count plots.
    counts_raw = pd.concat([pv_counts_raw, wind_counts_raw], ignore_index=True)
    counts_final = pd.concat([pv_counts_final, wind_counts_final], ignore_index=True)
    plot_counts(counts_raw, "PV", outdir / "pv_scenario_counts_by_year_raw.png")
    plot_counts(counts_raw, "Wind", outdir / "wind_scenario_counts_by_year_raw.png")
    plot_counts(counts_final, "PV", outdir / "pv_scenario_counts_by_year_interpolated.png")
    plot_counts(counts_final, "Wind", outdir / "wind_scenario_counts_by_year_interpolated.png")

    # Wright-law PV and wind cost estimation.
    if args.estimate_costs:
        print("\nEstimating PV and wind costs using Wright's law...")

        cost_jobs = [
            {
                "technology": "PV",
                "tech_lower": "pv",
                "mean_capacity": pv_mean,
                "historical_path": args.historical_pv_cost_csv,
                "default_file": DEFAULT_PV_COST_FILE,
                "input_unit": args.pv_cost_input_unit,
                "manual_learning_rate": args.manual_pv_learning_rate,
                "base_cost_usd_per_kw": args.base_pv_cost_usd_per_kw,
                "anchor_year": args.pv_cost_anchor_year,
            },
            {
                "technology": "Wind",
                "tech_lower": "wind",
                "mean_capacity": wind_mean,
                "historical_path": args.historical_wind_cost_csv,
                "default_file": DEFAULT_WIND_COST_FILE,
                "input_unit": args.wind_cost_input_unit,
                "manual_learning_rate": args.manual_wind_learning_rate,
                "base_cost_usd_per_kw": args.base_wind_cost_usd_per_kw,
                "anchor_year": args.wind_cost_anchor_year,
            },
        ]

        for job in cost_jobs:
            technology = job["technology"]
            tech_lower = job["tech_lower"]
            print(f"\n--- {technology} cost estimation ---")

            historical, historical_source = read_historical_cost_data(
                path=job["historical_path"],
                technology=technology,
                default_filename=job["default_file"],
                input_unit=job["input_unit"],
            )

            # For PV, keep only historical cost data from 2010 onward.
            if historical is not None and technology == "PV":
                historical = historical[historical["year"] >= 2010].copy()

            if historical is None:
                if job["manual_learning_rate"] is None:
                    raise ValueError(
                        f"No historical {technology} cost file was found. Place {job['default_file']} in the same "
                        f"folder as the script, pass --historical-{tech_lower}-cost-csv, or use "
                        f"--manual-{tech_lower}-learning-rate with --base-{tech_lower}-cost-usd-per-kw."
                    )
                print(f"No historical {technology} cost data found; using manual learning rate only.")
                fit_data = pd.DataFrame()
            else:
                historical["source"] = historical_source
                historical.to_csv(outdir / f"{tech_lower}_historical_cost_data_used.csv", index=False)
                print(f"Historical {technology} data source: {historical_source}")
                print(
                    f"Historical {technology} cost years: "
                    f"{int(historical['year'].min())}-{int(historical['year'].max())}"
                )
                print(
                    f"Historical {technology} cost unit handling: "
                    f"{historical['assumed_input_unit'].iloc[0]}"
                )

                fit_data = prepare_wright_fit_data(
                    historical=historical,
                    mean_capacity=job["mean_capacity"],
                    technology=technology,
                    fit_start_year=args.wright_fit_start_year,
                    fit_end_year=args.wright_fit_end_year,
                )
                fit_data.to_csv(outdir / f"{tech_lower}_wright_fit_data.csv", index=False)

            if job["manual_learning_rate"] is not None:
                params = manual_wright_parameters(
                    historical=historical,
                    technology=technology,
                    learning_rate=job["manual_learning_rate"],
                    base_cost_usd_per_kw=job["base_cost_usd_per_kw"],
                )
            else:
                params = estimate_wright_learning_from_fit_data(
                    fit_data=fit_data,
                    historical=historical,
                    technology=technology,
                )

            params_df = pd.DataFrame([params])
            params_df.to_csv(outdir / f"{tech_lower}_wright_learning_parameters.csv", index=False)

            cost_projection = estimate_cost_projection_by_group(
                mean_capacity=job["mean_capacity"],
                params=params,
                technology=technology,
                target_end_year=args.cost_end_year,
                anchor_year=job["anchor_year"],
            )
            cost_projection.to_csv(outdir / f"{tech_lower}_wright_cost_projection_by_group.csv", index=False)

            plot_cost_projection(
                technology=technology,
                historical=historical,
                projection=cost_projection,
                output_path=outdir / f"{tech_lower}_wright_cost_projection_to_2070.png",
                target_end_year=args.cost_end_year,
                log_y=False,
            )

            plot_cost_projection(
                technology=technology,
                historical=historical,
                projection=cost_projection,
                output_path=outdir / f"{tech_lower}_wright_cost_projection_to_2070_log.png",
                target_end_year=args.cost_end_year,
                log_y=True,
            )

            plot_wright_experience_curve_fit(
                technology=technology,
                fit_data=fit_data,
                params=params,
                output_path=outdir / f"{tech_lower}_wright_experience_curve_fit.png",
            )

            print(f"\n{technology} Wright-law parameters:")
            print(params_df.T.to_string(header=False))
            print(f"\n{technology} cost projection in final year:")
            final_year = cost_projection["year"].max()
            capacity_col = f"{tech_lower}_capacity_gw"
            print(
                cost_projection[cost_projection["year"] == final_year][
                    ["group", "year", capacity_col, "cost_usd_per_kw"]
                ].to_string(index=False)
            )

    print("\nPV dictionary groups and scenario counts:")
    print({group: len(items) for group, items in pv_dictionary.items()})
    print("Wind dictionary groups and scenario counts:")
    print({group: len(items) for group, items in wind_dictionary.items()})

    print("\nImportant diagnostic files:")
    print(f"  {outdir / 'pv_scenario_counts_by_year_raw.csv'}")
    print(f"  {outdir / 'pv_scenario_counts_by_year_interpolated.csv'}")
    print(f"  {outdir / 'wind_scenario_counts_by_year_raw.csv'}")
    print(f"  {outdir / 'wind_scenario_counts_by_year_interpolated.csv'}")

    if args.estimate_costs:
        print("\nImportant cost files:")
        print(f"  {outdir / 'pv_wright_learning_parameters.csv'}")
        print(f"  {outdir / 'pv_wright_cost_projection_by_group.csv'}")
        print(f"  {outdir / 'pv_wright_cost_projection_to_2070.png'}")
        print(f"  {outdir / 'pv_wright_cost_projection_to_2070_log.png'}")
        print(f"  {outdir / 'wind_wright_learning_parameters.csv'}")
        print(f"  {outdir / 'wind_wright_cost_projection_by_group.csv'}")
        print(f"  {outdir / 'wind_wright_cost_projection_to_2070.png'}")
        print(f"  {outdir / 'wind_wright_cost_projection_to_2070_log.png'}")

    print(f"\nSaved outputs in: {outdir.resolve()}")

    # In an interactive notebook, after running with %runfile, you can inspect:
    #   pv_dictionary[BY_2070]
    #   pv_dictionary[NOT_BY_2070]
    #   wind_dictionary[BY_2070]
    #   wind_dictionary[NOT_BY_2070]
    #   pv_records_final
    #   wind_records_final


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise
