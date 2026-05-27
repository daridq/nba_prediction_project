# NBA Prediction Project

## Project Overview
End-to-end ML pipeline predicting NBA game outcomes (binary classification).
- 0 = Home team wins
- 1 = Away team wins

## Data
- Source: nba_api Python package
- Timeframe: Last 5 seasons (reflects modern NBA cap-era dynamics)
- Row structure: One row per game with mirrored home/away features

## Pipeline Phases
1. Data Scraping
2. Data Exploration and Cleaning
3. Feature Engineering
4. Model Creation
5. Model Evaluation

## Planned Models (in order)
1. Heuristic baseline (always predict home team wins)
2. Logistic Regression
3. Single Decision Tree
4. Random Forest
5. XGBoost
6. Stacking Ensemble (stretch goal)

## Feature Categories
- Pre-game: matchup, home/away, player availability, injury status
- Form: rolling averages of key stats (last 5 games)
- Historical: head-to-head record (last 5 matchups)
- Contextual: rest days, home/away performance splits

## Conventions
- Language: Python
- Raw data is read-only — all transformations output to data/processed
- Suffix convention: _home and _away for mirrored team features
- Always show a plan before making changes
- Explain what each function does in comments