# Chronic Disease Risk Explorer

An interactive dashboard for exploring how demographic, clinical, lifestyle, and symptom indicators vary alongside heart disease, diabetes, and stroke outcomes.

> **Educational project, not a clinical tool.** The built-in dataset is simulated synthetic data. It does not represent real patients, establish medical evidence, provide diagnosis, or predict an individual's health. Associations do not prove causation.

## Demo

**Live app:** Add the Streamlit Community Cloud URL here after deploying (see [Deploy online](#deploy-online)).

## What it includes

- Prevalence KPIs and filters for age, BMI category, and exercise level.
- Outcome prevalence comparisons by age group and BMI category.
- Lifestyle and symptom comparisons plus a correlation matrix.
- CSV upload, filtered data preview, and filtered CSV download.
- Synthetic demonstration data generated reproducibly by the app; no patient data required to run it.

## Run locally

Requires Python 3.11 or newer (Python 3.12 recommended).

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local address printed in the terminal (usually http://localhost:8501). On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## CSV format for your own approved data

Upload a CSV in the dashboard using these exact column names:

| Column | Meaning / accepted values |
|---|---|
| `Age` | Age in years (number) |
| `BMI` | Body mass index (number) |
| `BloodPressure` | Systolic blood pressure in mmHg (number) |
| `Cholesterol` | Cholesterol level in the dataset's documented unit (number) |
| `Glucose` | Glucose level in the dataset's documented unit (number) |
| `Smoking`, `AlcoholUse`, `Fatigue`, `ChestPain`, `Dizziness` | Binary 0/1 or Yes/No |
| `ExerciseLevel` | Category such as Low, Moderate, High |
| `HeartDisease`, `Diabetes`, `Stroke` | Binary outcome 0/1 or Yes/No |

`PatientID` is optional and is only a display field. Do not upload names, addresses, phone numbers, medical record numbers, or other identifying/private health information to a public demo. Check the dataset license, consent, and course rules before sharing data. The app processes an uploaded CSV in memory for that session and does not persist it.

## Deploy online with Streamlit Community Cloud

1. Create a **public GitHub repository** named `chronic-disease-risk-explorer` (or another available name). Do not initialize it with a README if you already have this local project.
2. From this project folder, run the following in PowerShell, replacing `YOUR_GITHUB_USERNAME` with your account name:

   ```powershell
   git add .
   git commit -m "Build Chronic Disease Risk Explorer dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/chronic-disease-risk-explorer.git
   git push -u origin main
   ```

   If `origin` already exists, use `git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/chronic-disease-risk-explorer.git` instead of `git remote add`.
3. Sign in at [share.streamlit.io](https://share.streamlit.io/) with GitHub and authorize access to the repository.
4. Choose **Create app**, select the repository, branch `main`, and entrypoint `app.py`; then deploy.
5. When deployment finishes, copy the generated `https://....streamlit.app` address into the **Live app** section above and submit that URL with the GitHub repository link.

The demo URL cannot be reserved or created before the app is deployed from your GitHub account. Community Cloud assigns it during deployment. You can optionally choose a short subdomain if it is available.

## Suggested repository contents

```text
chronic-disease-risk-explorer/
├── app.py                 # dashboard
├── requirements.txt       # pinned Python dependencies
├── README.md              # project, data, setup, and deployment guide
├── .gitignore             # excludes local secrets and environments
└── LICENSE                # add a license only if your course permits it
```

## Suggested project description for GitHub

> Interactive dashboard for exploring chronic disease prevalence and demographic, clinical, lifestyle, and symptom patterns using synthetic demonstration data.

## Limitations and responsible use

- Simulated records are for demonstrating dashboard interactions only; any patterns are artificial.
- Charts show descriptive group differences and correlations, not causal relationships or validated clinical risk.
- No model is trained, and the app does not generate a patient-specific risk score.
- A real analysis requires a documented, appropriately licensed dataset, data-quality checks, and careful interpretation of missingness, sampling, confounding, and outcome definitions.

## Credits

Created as a college course project. Add course, author, dataset, and instructor acknowledgements as appropriate before submission.
