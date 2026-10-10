# Technical Plan: Used-Car Price Estimator

This describes a beginner-friendly Python app. No code yet — just the plan.

## Stack
- **pandas**: loads and cleans `used-cars.csv`.
- **scikit-learn** (`RandomForestRegressor`): learns prices from the listings.
- **Streamlit**: the browser screen where the user enters car details and sees the estimate.

## Files to Create
- **`app.py`**: the whole app — data loading, cleaning, model training, and the Streamlit screen. One file keeps it simple for a beginner project.
- **`requirements.txt`**: pins the libraries so local setup and Railway install the same thing.
- Uses existing files: `used-cars.csv` (the data), `PRD.md` / `FUNCTIONAL.md` (what to build).

## Model Inputs (CSV Columns)
Target (what the model learns to predict):
- `price_usd`

Features (what the model learns from):
- `brand`, `model`, `year`, `mileage_miles`, `fuel_type`, `transmission`, `accident_reported`, `clean_title`

Cleaning before training (because the raw data is messy):
- Normalize `transmission` free text (60 raw variants like `A/T`, `Automatic`, `8-Speed A/T`) into a small set of groups such as automatic, manual, and CVT/other.
- Normalize `model` text (lowercase, trim extra trim-level wording) so similar models match.
- Treat `Unknown` in `fuel_type` and `clean_title` as its own category, not as missing data.
- Keep `year` and `mileage_miles` as numbers.

## Training When the App Starts
1. Load `used-cars.csv` with pandas.
2. Apply the cleaning steps above and turn categories into numbers the model can use (one-hot encoding).
3. Split the listings into a training set and a small held-back test set, so we can check accuracy.
4. Train a `RandomForestRegressor` on the training set.
5. Score it on the test set (average prediction error) and log the result; this is the "how we'll know it works" check from the PRD.
6. Keep the trained model in memory. When a user submits a car, the app cleans the inputs the same way, asks the model for a prediction (the estimated price), derives the low–high range from how much the individual trees disagree, and picks the top factors from what the model found most influential.

Training happens once at startup and takes seconds on ~3,900 rows, so there is no separate training step or saved model file for this version.

## Libraries Needed (`requirements.txt`)
- `pandas` — data loading and cleaning.
- `scikit-learn` — the RandomForest model.
- `streamlit` — the UI.
- (Streamlit pulls in its own web dependencies automatically.)

## Run Locally on Windows
From the project root, in PowerShell:

1. Activate the virtual environment: `.\.venv\Scripts\Activate.ps1`
2. Install libraries: `pip install -r requirements.txt`
3. Start the app: `streamlit run app.py`
4. Open the address Streamlit prints (usually `http://localhost:8501`) in a browser.

## Later Deploy to Railway
Nothing extra to build now; the same app deploys with two things:
- `requirements.txt` so Railway installs pandas, scikit-learn, and Streamlit.
- A start command so Railway launches the Streamlit server, listening on Railway's port:
  `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

The dataset file `used-cars.csv` deploys with the code, and training still happens at startup exactly as it does locally.
