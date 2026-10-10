"""Used-car price estimator.

Loads used-cars.csv with pandas, trains a RandomForestRegressor on startup,
and serves a Streamlit screen for price estimates.
"""

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

CSV_PATH = "used-cars.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42

CATEGORICAL_COLS = ["brand", "model_clean", "fuel_type", "trans_group",
                    "accident_reported", "clean_title"]
NUMERIC_COLS = ["year", "mileage_miles"]
TARGET_COL = "price_usd"

FUEL_TYPES = ["Diesel", "E85 Flex Fuel", "Gasoline", "Hybrid", "Plug-In Hybrid"]
TRANS_GROUPS = ["Automatic", "Manual", "CVT", "Other"]


def normalize_transmission(raw):
    """Map the 60 messy transmission labels into 4 groups."""
    t = str(raw).upper()
    if "CVT" in t:
        return "CVT"
    if "AUTOMATIC" in t or "A/T" in t or "DUAL SHIFT" in t:
        return "Automatic"
    if "M/T" in t or t == "MANUAL" or t.startswith("MANUAL ") or t.endswith(" MANUAL"):
        return "Manual"
    if t.strip() in {"F", "2"}:
        return "Other"
    if "MANUAL" in t:
        return "Automatic"  # e.g. automatics with a "manual mode" mention
    return "Other"


def clean_model(raw):
    """Lowercase and trim model text so similar models match."""
    return " ".join(str(raw).lower().split())


def load_data():
    df = pd.read_csv(CSV_PATH)
    df["trans_group"] = df["transmission"].apply(normalize_transmission)
    df["model_clean"] = df["model"].apply(clean_model)
    return df


def train_model(df):
    """Train once at startup; return model, encoder, test MAE, and reference stats."""
    features = CATEGORICAL_COLS + NUMERIC_COLS
    X_cat = df[CATEGORICAL_COLS]
    X_num = df[NUMERIC_COLS]
    y = df[TARGET_COL]

    encoder = OneHotEncoder(handle_unknown="ignore")
    X_cat_enc = encoder.fit_transform(X_cat)
    X_all = np.hstack([X_cat_enc.toarray(), X_num.to_numpy()])

    X_train, X_test, y_train, y_test = train_test_split(
        X_all, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    model = RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1)
    model.fit(X_train, y_train)
    mae = float(np.mean(np.abs(model.predict(X_test) - y_test)))
    print(f"Model trained on {len(X_train)} listings. Test MAE: ${mae:,.0f}")

    stats = {
        "median_price": float(y.median()),
        "median_mileage": float(df["mileage_miles"].median()),
        "median_year": float(df["year"].median()),
        "importances": model.feature_importances_,
        "cat_names": list(encoder.get_feature_names_out(CATEGORICAL_COLS)),
    }
    return model, encoder, mae, stats


def encode_inputs(encoder, row):
    cat = encoder.transform(row[CATEGORICAL_COLS]).toarray()
    num = row[NUMERIC_COLS].to_numpy()
    return np.hstack([cat, num])


def predict_with_range(model, X):
    """Estimate from the forest mean; low-high from per-tree 10th/90th percentiles."""
    tree_preds = np.array([tree.predict(X) for tree in model.estimators_])
    estimate = float(tree_preds.mean())
    low = float(np.percentile(tree_preds, 10))
    high = float(np.percentile(tree_preds, 90))
    return estimate, low, high


def top_factors(stats, inputs):
    """Pick the 3 most influential input groups and explain them plainly."""
    importances = stats["importances"]
    cat_names = stats["cat_names"]
    n_cat = len(cat_names)
    grouped = {}
    # Aggregate one-hot importances back to original columns.
    for i, name in enumerate(cat_names):
        for col in CATEGORICAL_COLS:
            if name.startswith(col + "_"):
                grouped[col] = grouped.get(col, 0.0) + importances[i]
                break
    for j, col in enumerate(NUMERIC_COLS):
        grouped[col] = importances[n_cat + j]

    explanations = {
        "mileage_miles": (
            f"Mileage ({inputs['mileage_miles']:,} mi vs typical "
            f"{stats['median_mileage']:,.0f} mi)"
            + (" lowered the estimate" if inputs["mileage_miles"] > stats["median_mileage"]
               else " raised the estimate")
        ),
        "year": (
            f"Model year ({inputs['year']} vs typical {stats['median_year']:.0f})"
            + (" raised the estimate" if inputs["year"] >= stats["median_year"]
               else " lowered the estimate")
        ),
        "brand": f"Brand ({inputs['brand']}) priced vs the market average",
        "model_clean": f"Model ({inputs.get('model', inputs['model_clean'])}) priced vs similar cars",
        "fuel_type": f"Fuel type ({inputs['fuel_type']}) adjusted the estimate",
        "trans_group": f"Transmission ({inputs['trans_group']}) adjusted the estimate",
        "accident_reported": (
            "Accident reported lowered the estimate"
            if inputs["accident_reported"] == "Yes"
            else "Clean accident history supported the estimate"
        ),
        "clean_title": (
            "Clean title supported the estimate"
            if inputs["clean_title"] == "Yes"
            else "Unknown title status added uncertainty"
        ),
    }
    ranked = sorted(grouped.items(), key=lambda kv: kv[1], reverse=True)[:3]
    return [explanations[col] for col, _ in ranked]


df = load_data()
MODEL, ENCODER, TEST_MAE, STATS = train_model(df)


def main():
    st.title("Used-Car Price Estimator")
    st.write("Enter the car's details to get a fair-price estimate from real listings.")

    brands = sorted(df["brand"].unique())
    brand = st.selectbox("Brand", brands)

    brand_models = sorted(df.loc[df["brand"] == brand, "model"].unique())
    model = st.selectbox("Model", brand_models)

    year = st.number_input("Year", min_value=1998, max_value=2024, value=2015, step=1)
    mileage = st.number_input("Mileage (miles)", min_value=100, max_value=300000,
                              value=75000, step=1000)

    fuel = st.selectbox("Fuel type", FUEL_TYPES)
    trans = st.selectbox("Transmission", TRANS_GROUPS)
    accident = st.selectbox("Accident reported", ["No", "Yes"])
    title = st.selectbox("Clean title", ["Yes", "Unknown"])

    if st.button("Estimate price"):
        row = pd.DataFrame([{
            "brand": brand,
            "model_clean": clean_model(model),
            "year": int(year),
            "mileage_miles": int(mileage),
            "fuel_type": fuel,
            "trans_group": trans,
            "accident_reported": accident,
            "clean_title": title,
        }])
        inputs = row.iloc[0].to_dict()
        inputs["model"] = model
        X = encode_inputs(ENCODER, row)
        estimate, low, high = predict_with_range(MODEL, X)

        st.subheader(f"Estimated price: ${estimate:,.0f}")
        st.write(f"Expected range: ${low:,.0f} – ${high:,.0f}")
        st.write("Top factors:")
        for factor in top_factors(STATS, inputs):
            st.write(f"- {factor}")


if __name__ == "__main__":
    main()
