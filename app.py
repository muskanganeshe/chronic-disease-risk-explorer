from __future__ import annotations
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Chronic Disease Risk Explorer", page_icon="🩺", layout="wide")
OUTCOMES = ["HeartDisease", "Diabetes", "Stroke"]
REQUIRED = ["Age", "BMI", "BloodPressure", "Cholesterol", "Glucose", "Smoking", "AlcoholUse", "ExerciseLevel", "Fatigue", "ChestPain", "Dizziness", *OUTCOMES]

@st.cache_data
def sample_data(n=2400, seed=42):
    """Reproducible synthetic records for demonstrating the dashboard."""
    rng = np.random.default_rng(seed)
    age = rng.integers(18, 86, n)
    bmi = np.clip(rng.normal(27 + (age - 45) * .025, 5.2, n), 15, 52).round(1)
    smoking = rng.binomial(1, .20, n)
    alcohol = rng.binomial(1, .25, n)
    exercise = rng.choice(["Low", "Moderate", "High"], n, p=[.36, .43, .21])
    penalty = np.select([exercise == "Low", exercise == "Moderate"], [1.3, .5], default=0)
    bp = np.clip(rng.normal(112 + .48 * age + .55 * (bmi - 25) + 5 * smoking, 14, n), 82, 220).round().astype(int)
    chol = np.clip(rng.normal(178 + .42 * age + 1.1 * (bmi - 25) + 7 * smoking, 31, n), 90, 360).round().astype(int)
    glucose = np.clip(rng.normal(88 + .35 * age + 1.35 * (bmi - 25) + penalty * 2, 18, n), 55, 260).round().astype(int)
    sigmoid = lambda x: 1 / (1 + np.exp(-x))
    diabetes = rng.binomial(1, sigmoid(-4.1 + .045 * (age - 40) + .11 * (bmi - 25) + .018 * (glucose - 100) + .35 * (exercise == "Low")))
    heart = rng.binomial(1, sigmoid(-4.5 + .047 * (age - 40) + .018 * (bp - 120) + .009 * (chol - 190) + .55 * smoking + .45 * diabetes))
    stroke = rng.binomial(1, sigmoid(-5 + .055 * (age - 40) + .024 * (bp - 120) + .55 * diabetes + .35 * smoking))
    fatigue = rng.binomial(1, sigmoid(-1.7 + .025 * (age - 40) + .25 * (exercise == "Low") + .38 * diabetes))
    chest = rng.binomial(1, sigmoid(-3.1 + .035 * (age - 40) + .75 * heart + .25 * smoking))
    dizzy = rng.binomial(1, sigmoid(-2.7 + .018 * (bp - 120) + .45 * stroke + .2 * diabetes))
    return pd.DataFrame({"PatientID": [f"SYN-{i:05d}" for i in range(1, n+1)], "Age": age, "BMI": bmi, "BloodPressure": bp, "Cholesterol": chol, "Glucose": glucose, "Smoking": smoking, "AlcoholUse": alcohol, "ExerciseLevel": exercise, "Fatigue": fatigue, "ChestPain": chest, "Dizziness": dizzy, "HeartDisease": heart, "Diabetes": diabetes, "Stroke": stroke})

def clean_data(df):
    df = df.copy()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing: return df, missing
    nums = [c for c in REQUIRED if c != "ExerciseLevel"]
    for c in nums: df[c] = pd.to_numeric(df[c].replace({"Yes": 1, "No": 0, "yes": 1, "no": 0, True: 1, False: 0}), errors="coerce")
    return df.dropna(subset=REQUIRED).copy(), []

st.title("🩺 Chronic Disease Risk Explorer")
st.caption("Interactive exploration of chronic disease patterns and health indicators")
st.warning("Educational demo only. Default records are synthetic and do not represent real patients. This dashboard does not diagnose, predict individual risk, or replace clinical judgment.")
with st.sidebar:
    st.header("Data and filters")
    upload = st.file_uploader("Upload a CSV (optional)", type="csv", help="Use the column names in README. Do not upload patient identifiers.")
    if upload:
        try: raw, missing = clean_data(pd.read_csv(upload)); source = "Uploaded CSV"
        except Exception as exc: st.error(f"Could not read CSV: {exc}"); st.stop()
        if missing: st.error("Missing required columns: " + ", ".join(missing)); st.stop()
        if raw.empty: st.error("No complete records found. Check required values."); st.stop()
    else: raw, _ = clean_data(sample_data()); source = "Synthetic demonstration data"
    st.caption(f"Source: **{source}** · {len(raw):,} records")
    age_range = st.slider("Age range", int(raw.Age.min()), int(raw.Age.max()), (int(raw.Age.min()), int(raw.Age.max())))
    bmi_group = st.selectbox("BMI category", ["All", "Underweight (<18.5)", "Healthy (18.5–24.9)", "Overweight (25–29.9)", "Obesity (≥30)"])
    exercise_group = st.selectbox("Exercise level", ["All", *sorted(raw.ExerciseLevel.astype(str).unique())])

df = raw[raw.Age.between(*age_range)].copy()
if bmi_group != "All":
    ranges = {"Underweight (<18.5)": (0, 18.5), "Healthy (18.5–24.9)": (18.5, 25), "Overweight (25–29.9)": (25, 30), "Obesity (≥30)": (30, np.inf)}
    lo, hi = ranges[bmi_group]; df = df[(df.BMI >= lo) & (df.BMI < hi)]
if exercise_group != "All": df = df[df.ExerciseLevel.astype(str) == exercise_group]
if df.empty: st.info("No records match these filters. Adjust the selections in the sidebar."); st.stop()

st.subheader("Population snapshot")
cols = st.columns(5)
cols[0].metric("Patients", f"{len(df):,}")
for i, outcome in enumerate(OUTCOMES, 1): cols[i].metric(outcome.replace("Disease", " disease"), f"{df[outcome].mean()*100:.1f}%")
cols[4].metric("Mean BMI", f"{df.BMI.mean():.1f}")
tab1, tab2, tab3 = st.tabs(["Disease patterns", "Risk factors", "Data preview"])
with tab1:
    left, right = st.columns(2)
    prev = pd.DataFrame({"Condition": ["Heart disease", "Diabetes", "Stroke"], "Prevalence (%)": [df[c].mean()*100 for c in OUTCOMES]})
    left.plotly_chart(px.bar(prev, x="Condition", y="Prevalence (%)", color="Condition", title="Condition prevalence in selected group", text_auto=".1f"), use_container_width=True)
    ages = df.assign(AgeGroup=pd.cut(df.Age, [0, 29, 44, 59, 74, 120], labels=["18–29", "30–44", "45–59", "60–74", "75+"])).groupby("AgeGroup", observed=False)[OUTCOMES].mean().mul(100).reset_index().melt("AgeGroup", var_name="Condition", value_name="Prevalence (%)")
    right.plotly_chart(px.line(ages, x="AgeGroup", y="Prevalence (%)", color="Condition", markers=True, title="Prevalence by age group"), use_container_width=True)
    bmi = df.assign(BMICategory=pd.cut(df.BMI, [-np.inf, 18.5, 25, 30, np.inf], labels=["Underweight", "Healthy", "Overweight", "Obesity"])).groupby("BMICategory", observed=False)[OUTCOMES].mean().mul(100).reset_index().melt("BMICategory", var_name="Condition", value_name="Prevalence (%)")
    st.plotly_chart(px.bar(bmi, x="BMICategory", y="Prevalence (%)", color="Condition", barmode="group", title="Condition prevalence by BMI category"), use_container_width=True)
with tab2:
    left, right = st.columns(2)
    life = df.groupby("ExerciseLevel", observed=False)[OUTCOMES].mean().mul(100).reset_index().melt("ExerciseLevel", var_name="Condition", value_name="Prevalence (%)")
    left.plotly_chart(px.bar(life, x="ExerciseLevel", y="Prevalence (%)", color="Condition", barmode="group", title="Disease prevalence by exercise level"), use_container_width=True)
    indicators = []
    for label, c in [("Smoking", "Smoking"), ("Alcohol use", "AlcoholUse"), ("Fatigue", "Fatigue"), ("Chest pain", "ChestPain"), ("Dizziness", "Dizziness")]:
        for outcome in OUTCOMES:
            group = df[df[c] == 1]
            indicators.append({"Indicator": label, "Condition": outcome, "Prevalence (%)": group[outcome].mean()*100 if len(group) else 0})
    right.plotly_chart(px.bar(pd.DataFrame(indicators), x="Indicator", y="Prevalence (%)", color="Condition", barmode="group", title="Condition prevalence when indicator is reported"), use_container_width=True)
    corr = df[["Age", "BMI", "BloodPressure", "Cholesterol", "Glucose", "Smoking", "AlcoholUse", "Fatigue", "ChestPain", "Dizziness", *OUTCOMES]].corr(numeric_only=True)
    st.plotly_chart(px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r", title="Correlation matrix (association, not causation)"), use_container_width=True)
with tab3:
    st.caption("Showing at most 100 filtered records. Uploaded CSV values are not saved by this app.")
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)
    st.download_button("Download filtered rows as CSV", df.to_csv(index=False).encode("utf-8"), "healthrisk_filtered.csv", "text/csv")
st.caption("Group differences and correlations are descriptive. Synthetic demo relationships are simulated and are not medical evidence.")
