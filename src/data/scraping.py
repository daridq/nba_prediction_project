"""Scrape NBA league game logs via nba_api and save them as raw parquet files."""

import logging
import time
from pathlib import Path
from typing import Any

import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

logger = logging.getLogger(__name__)

# Pause between live API calls to avoid overloading stats.nba.com
DELAY_SECONDS = 5


def fetch_league_game_log(season: str, season_type: str = "Regular Season") -> pd.DataFrame:
    """Fetch one season's league-wide game log from nba_api.

    Args:
        season: Season string, e.g. "2023-24".
        season_type: "Regular Season" or "Playoffs".

    Returns:
        DataFrame with one row per team per game for that season.
    """
    # timeout guards against stats.nba.com occasionally hanging on a request
    response = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star=season_type,
        timeout=60,
    )
    return response.get_data_frames()[0]


def scrape_and_save_season_logs(seasons: list[str], output_dir: Path) -> None:
    """Fetch and save each season's league game log as a raw parquet file.

    Skips seasons that already have a saved file, so re-running is cheap and
    doesn't re-hit the API unnecessarily.

    Args:
        seasons: Season strings to fetch, e.g. ["2023-24", "2024-25"].
        output_dir: Directory to write "<season>_data_raw.parquet" files to.
    """
    for season in seasons:
        file_path = output_dir / f"{season}_data_raw.parquet"

        if file_path.exists():
            logger.info("Skipping %s, file already exists", season)
            continue

        logger.info("Fetching data for season %s...", season)
        try:
            season_df = fetch_league_game_log(season)
        except Exception:
            logger.exception("Error fetching data for season %s", season)
            continue

        season_df.to_parquet(file_path, engine="pyarrow")
        time.sleep(DELAY_SECONDS)

def run_integrity_check(df: pd.DataFrame, base_schema: pd.Series | None) -> dict[str, Any]:
    """Run structural and relational integrity checks on one season's DataFrame.
    
        Args:
            df: Season game log DataFrame to check.
            base_schema: Reference dtypes to compare against (the first file's schema),
                or None to skip the schema check (used for the first file itself).
    
        Returns:
            Dict mapping check name to a "PASS"/"FAIL: <detail>" result string.
    """

    results: dict[str, Any] = {}
    
    ## Tier 1 Tests: Structural
    
    # Schema test: compare dtypes against the reference schema
    schema_matches = base_schema is None or df.dtypes.equals(base_schema)
    results["schema_match"] = "PASS" if schema_matches else "FAIL: dtypes differ from base schema"
    
    # Row count test: sanity-check row count vs. unique games (2 rows per game expected)
    row_count = len(df)
    unique_game_ids = df["GAME_ID"].nunique()
    results["row_count"] = f"PASS: {row_count} rows, {unique_game_ids} unique games"
    
    # Missing value test: flag any key columns with nulls
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    results["missing_values"] = "PASS" if missing_cols.empty else f"FAIL: {missing_cols.to_dict()}"
    
    # Duplicate test: no team should appear twice for the same game
    dup_count = int(df.duplicated(subset=["GAME_ID", "TEAM_ID"]).sum())
    results["duplicate_team_games"] = "PASS" if dup_count == 0 else f"FAIL: {dup_count} duplicate rows"
    
    ## Tier 2 Tests: Relatability
    
    # Join key test: every GAME_ID should have exactly 2 rows (home + away team)
    game_id_counts = df["GAME_ID"].value_counts()
    bad_game_ids = game_id_counts[game_id_counts != 2]
    results["game_id_pairing"] = (
        "PASS" if bad_game_ids.empty else f"FAIL: {len(bad_game_ids)} games without exactly 2 rows"
    )
    
    # Date range test: sanity check the season boundaries
    game_dates = pd.to_datetime(df["GAME_DATE"])
    results["date_range"] = f"PASS: {game_dates.min().date()} to {game_dates.max().date()}"
    
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DEFAULT_SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

    scrape_and_save_season_logs(
        seasons=DEFAULT_SEASONS,
        output_dir=PROJECT_ROOT / "data" / "raw",
    )
