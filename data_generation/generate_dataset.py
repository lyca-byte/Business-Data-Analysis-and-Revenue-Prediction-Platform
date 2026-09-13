"""
generate_dataset.py
--------------------
Generates a synthetic business revenue dataset for the
Business Data Analysis and Revenue Prediction Platform.

Output:
    data/raw/business_revenue_dataset.csv

Dataset size: 5,000 samples
Features    : 7 input features + 1 target variable (revenue)
"""

import numpy as np
import pandas as pd
import os


# ── Reproducibility ──────────────────────────────────────────────────────────
# Setting a fixed random seed ensures that every run of this script produces
# the exact same dataset. This is critical for reproducibility: your analysis
# notebooks, model training, and model evaluation will all reference the same
# underlying data.
RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


# ── Dataset configuration ─────────────────────────────────────────────────────
N_SAMPLES = 5_000


# ── Feature generation ────────────────────────────────────────────────────────
def generate_features(n: int, rng: np.random.Generator) -> dict:
    """
    Generate the 7 input features for the business dataset.

    Each feature uses a realistic range based on a mid-size business context.
    Some features have a slight positive correlation with each other to
    simulate real-world business data (e.g., companies that spend more on
    marketing also tend to spend more on advertising).
    """

    # Marketing Spend: USD 1,000 – 50,000
    # Drawn from a log-normal-influenced distribution so that most businesses
    # cluster around lower budgets, with fewer high-spend outliers.
    marketing_spend = rng.uniform(1_000, 50_000, n)

    # Advertising Spend: USD 500 – 30,000
    # Correlated with marketing_spend: businesses with higher marketing budgets
    # tend to also invest more in advertising.
    # Base component is independent; correlated component adds the relationship.
    advertising_base = rng.uniform(500, 20_000, n)
    advertising_spend = advertising_base + 0.2 * marketing_spend
    advertising_spend = np.clip(advertising_spend, 500, 30_000)

    # Website Traffic: 5,000 – 200,000 monthly visitors
    # Correlated with advertising_spend: more advertising drives more traffic.
    traffic_base = rng.uniform(5_000, 150_000, n)
    website_traffic = traffic_base + 0.8 * advertising_spend
    website_traffic = np.clip(website_traffic, 5_000, 200_000)

    # Number of Customers: 100 – 5,000
    # Loosely correlated with website_traffic: more visitors → more customers.
    customer_base = rng.uniform(100, 3_000, n)
    number_of_customers = customer_base + 0.005 * website_traffic
    number_of_customers = np.clip(number_of_customers, 100, 5_000)

    # Product Price: USD 10 – 500
    # Independent feature — price is set by the business, not driven by spend.
    product_price = rng.uniform(10, 500, n)

    # Discount Percentage: 0 – 50%
    # Independent feature — discount strategy varies across businesses.
    discount_percentage = rng.uniform(0, 50, n)

    # Previous Revenue: USD 20,000 – 500,000
    # Acts as an anchor for current revenue. Businesses with higher past
    # revenue tend to generate higher current revenue (momentum effect).
    previous_revenue = rng.uniform(20_000, 500_000, n)

    return {
        "marketing_spend": marketing_spend,
        "advertising_spend": advertising_spend,
        "website_traffic": website_traffic,
        "number_of_customers": number_of_customers,
        "product_price": product_price,
        "discount_percentage": discount_percentage,
        "previous_revenue": previous_revenue,
    }


# ── Revenue calculation ───────────────────────────────────────────────────────
def calculate_revenue(features: dict, rng: np.random.Generator) -> np.ndarray:
    """
    Calculate the Revenue target variable using a structured formula.

    Revenue is a linear combination of the input features plus:
        1. Multiplicative noise — simulates overall business unpredictability.
        2. Additive noise      — simulates measurement variance and
                                 unmodeled external factors.

    Coefficient design rationale:
        marketing_spend     (+0.80) Strong positive effect — direct ROI
        advertising_spend   (+0.60) Strong positive effect — direct ROI
        website_traffic     (+0.05) Moderate positive effect per visitor
        number_of_customers (+20.0) Each customer contributes ~$20 to revenue
        product_price       (+15.0) Higher price → higher revenue per sale
        discount_percentage (-200)  Each 1% discount reduces revenue by ~$200
        previous_revenue    (+0.30) 30% of past revenue carries forward
        intercept           (+15000) Base revenue floor
    """
    n = len(features["marketing_spend"])

    base_revenue = (
          0.80 * features["marketing_spend"]
        + 0.60 * features["advertising_spend"]
        + 0.05 * features["website_traffic"]
        + 20.0 * features["number_of_customers"]
        + 15.0 * features["product_price"]
        - 200.0 * features["discount_percentage"]
        + 0.30 * features["previous_revenue"]
        + 15_000
    )

    # Multiplicative noise: factor between 0.85 and 1.15
    # This scales the entire revenue up or down by ±15%, simulating
    # real-world variation in how efficiently inputs convert to revenue.
    multiplicative_noise = rng.uniform(0.85, 1.15, n)

    # Additive noise: standard deviation of 8,000 USD
    # This adds independent random variation on top of the scaled revenue,
    # representing factors not captured by the features (e.g., seasonality,
    # external market conditions, one-off events).
    additive_noise = rng.normal(0, 8_000, n)

    revenue = base_revenue * multiplicative_noise + additive_noise

    # Clip to a realistic minimum — revenue cannot be negative
    revenue = np.clip(revenue, 5_000, None)

    return revenue


# ── Dataset validation ────────────────────────────────────────────────────────
def validate_dataset(df: pd.DataFrame) -> None:
    """
    Run basic validation checks on the generated dataset.
    Raises an AssertionError if any check fails.
    """
    print("\n-- Dataset Validation ------------------------------------------")

    # Shape
    assert df.shape == (N_SAMPLES, 8), f"Unexpected shape: {df.shape}"
    print(f"  Shape                : {df.shape[0]} rows x {df.shape[1]} columns  OK")

    # No missing values
    missing = df.isnull().sum().sum()
    assert missing == 0, f"Found {missing} missing values"
    print(f"  Missing values       : {missing}  OK")

    # No duplicate rows
    duplicates = df.duplicated().sum()
    assert duplicates == 0, f"Found {duplicates} duplicate rows"
    print(f"  Duplicate rows       : {duplicates}  OK")

    # Feature range checks
    assert df["marketing_spend"].between(1_000, 50_000).all(), "marketing_spend out of range"
    assert df["advertising_spend"].between(500, 30_000).all(), "advertising_spend out of range"
    assert df["website_traffic"].between(5_000, 200_000).all(), "website_traffic out of range"
    assert df["number_of_customers"].between(100, 5_000).all(), "number_of_customers out of range"
    assert df["product_price"].between(10, 500).all(), "product_price out of range"
    assert df["discount_percentage"].between(0, 50).all(), "discount_percentage out of range"
    assert df["previous_revenue"].between(20_000, 500_000).all(), "previous_revenue out of range"
    assert (df["revenue"] >= 5_000).all(), "revenue contains values below minimum"
    print(f"  Feature ranges       : all within bounds  OK")

    # Revenue correlation sanity check (should be reasonably positive)
    corr_marketing = df["marketing_spend"].corr(df["revenue"])
    corr_customers = df["number_of_customers"].corr(df["revenue"])
    assert corr_marketing > 0.2, f"marketing_spend correlation too low: {corr_marketing:.3f}"
    assert corr_customers > 0.2, f"number_of_customers correlation too low: {corr_customers:.3f}"
    print(f"  Revenue correlations : marketing={corr_marketing:.3f}, customers={corr_customers:.3f}  OK")

    print("-- Validation passed -------------------------------------------\n")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  Business Revenue Dataset Generator")
    print("=" * 55)
    print(f"  Samples     : {N_SAMPLES:,}")
    print(f"  Random seed : {RANDOM_SEED}")
    print("=" * 55)

    # 1. Generate features
    print("\n[1/4] Generating features...")
    features = generate_features(N_SAMPLES, rng)

    # 2. Calculate revenue target
    print("[2/4] Calculating revenue target...")
    revenue = calculate_revenue(features, rng)

    # 3. Assemble DataFrame
    print("[3/4] Assembling dataset...")
    df = pd.DataFrame(features)
    df["revenue"] = revenue

    # Round to 2 decimal places for clean CSV output
    df = df.round(2)

    # 4. Validate
    validate_dataset(df)

    # 5. Save to CSV
    print("[4/4] Saving dataset...")
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    output_path = os.path.join(output_dir, "business_revenue_dataset.csv")
    os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"  Saved to : {os.path.normpath(output_path)}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")

    # 6. Print summary statistics
    print("\n-- Revenue Summary ---------------------------------------------")
    rev = df["revenue"]
    print(f"  Min    : ${rev.min():>12,.2f}")
    print(f"  Max    : ${rev.max():>12,.2f}")
    print(f"  Mean   : ${rev.mean():>12,.2f}")
    print(f"  Median : ${rev.median():>12,.2f}")
    print(f"  Std    : ${rev.std():>12,.2f}")
    print("----------------------------------------------------------------")

    print("\n-- Feature Correlations with Revenue ---------------------------")
    correlations = df.corr()["revenue"].drop("revenue").sort_values(ascending=False)
    for feature, corr in correlations.items():
        bar = "#" * int(abs(corr) * 20)
        sign = "+" if corr >= 0 else "-"
        print(f"  {feature:<25} {sign}{abs(corr):.3f}  {bar}")
    print("----------------------------------------------------------------")

    print("\nDataset generation complete.")


if __name__ == "__main__":
    main()
