"""Scrape NBA league game logs via nba_api and save them as raw parquet files."""

import logging
import time
from pathlib import Path

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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    DEFAULT_SEASONS = ["2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]

    scrape_and_save_season_logs(
        seasons=DEFAULT_SEASONS,
        output_dir=PROJECT_ROOT / "data" / "raw",
    )
