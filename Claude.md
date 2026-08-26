# NBA Prediction Project

## Project Overview
the NBA Prediction Project is an end-to-end machine learning pipeline project that takes in 2 team's historical information and predicts which NBA game outcomes as a binary classification. The goal of this project is to help the data scientist (me) develop real skills in creating pipelines with the help of AI codingl.

- The binary classification is as follows:
    - 0 = Home team wins
    - 1 = Away team wins
- Success = getting a 85-90% success rate for predictions as well as learn the pros and cons of choosing different models.
- This is a learning project for both building a machine learning model as well as for working with Claude Code so favor simple, inspectable solutions over clever ones.

## Data
- Source: nba_api Python package
- Timeframe: Last 5 seasons (reflects modern NBA cap-era dynamics)
- Row structure: One row per game with mirrored home/away features
- File structure: Experimentation of functions will be done in notebooks/. Training logs will be uploaded under logs/experiment/. 

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

- Open to learning more about other models after we finish creating the 6 goal models.

## Repository Context
- Type hints on every function signature, including return types
- Docstrings: one-line summary + Args/Returns, Google style

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
- Explain what each function does in comments.

## Security Context
- ANTHROPIC_API_KEY read from environment variable only — never written to
  code, config files, or committed anywhere. Fail loudly if unset.
- Never delete or overwrite raw log files — logs are the
  only copy of my activity history.