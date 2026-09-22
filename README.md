# 🚗 Otomoto Market Analysis & Car Price Prediction

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-0.14+-blue?style=flat)](https://www.statsmodels.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A comprehensive end-to-end analytical and predictive project featuring automated data collection (web scraping) from the **Otomoto** portal (Kraków automotive market), data cleaning, feature engineering, exploratory data analysis (EDA), and econometric multivariable log-linear regression modeling.

---

## 📌 Table of Contents
1. [Project Overview & Objectives](#-project-overview--objectives)
2. [Repository Structure](#-repository-structure)
3. [Data Pipeline & Feature Engineering](#-data-pipeline--feature-engineering)
4. [Exploratory Data Analysis (EDA) Insights](#-exploratory-data-analysis-eda-insights)
5. [Predictive Model (OLS Linear Regression)](#-predictive-model-ols-linear-regression)
6. [Tech Stack & Requirements](#-tech-stack--requirements)
7. [Getting Started & Usage](#-getting-started--usage)
8. [Dataset Schema](#-dataset-schema)
9. [Future Roadmap](#-future-roadmap)
10. [Legal & Ethical Considerations](#-legal--ethical-considerations)
11. [Author & Contact](#-author--contact)

---

## 🎯 Project Overview & Objectives

The primary objective of this project was to analyze the microstructure of the local used and new car market in the Kraków area and estimate a vehicle's market value based on key technical and operational parameters.

**Project Phases:**
1. **Data Acquisition:** Implemented a modular web scraper gathering raw advertisement metadata into JSON files, equipped with `User-Agent` header rotation and random request delays.
2. **Data Aggregation & Cleaning:** Currency normalization (EUR $\to$ PLN), regular expressions (`regex`) to extract engine displacement from raw text attributes, and hierarchical median imputation for missing values.
3. **Exploratory Data Analysis (EDA):** Investigated marginal distributions, skewness, correlation matrices, and market behavioral trends influenced by local regulations (such as Kraków's Clean Transport Zone — SCT).
4. **Econometric Modeling:** Validated Gauss-Markov Classical Ordinary Least Squares (OLS) assumptions, removed outliers, and fitted a log-linear model.

---

## 💡 Key Insights

Based on the exploratory data analysis and econometric modeling of **11,477 cleaned listings** (from an initial sample of 11,998)[cite: 1, 2], the project revealed several critical patterns regarding the local automotive market:

* **Severe Price Skewness & Log-Transformation**: The raw distribution of `Cena` (price) was heavily right-skewed[cite: 1], with a mean price of **~77,317 PLN** and a median of **47,000 PLN** (ranging up to nearly 1.6M PLN in the raw data)[cite: 1]. Most vehicle listings are concentrated below 100,000 PLN[cite: 1]. Applying a natural log transformation ($\ln(\text{Cena})$) was essential to stabilize residual variance and satisfy the linear assumption required for Ordinary Least Squares (OLS) estimation[cite: 1, 2].
* **Local Market Dynamics & Environmental Regulations**: Vehicles manufactured after 2010 constitute the core of the market[cite: 1], with an average production year of **2016** (median: 2017)[cite: 1]. There is a sharp decline in listings for cars produced before 2004–2005[cite: 1], reflecting regional consumer adjustments and anticipation of the Clean Transport Zone (Strefa Czystego Transportu – SCT) regulations in Kraków[cite: 1].
* **Determinants of Valuation (Depreciation vs. Age & Mileage)**: 
  * `Rocznik` (year of manufacture) shows a moderate positive relationship with price[cite: 1], while `Przebieg` (mileage, averaging ~142,000 km) exhibits a moderate negative correlation with price[cite: 1].
  * There is a strong negative collinearity between vehicle age and mileage[cite: 1], validating the intuition that higher wear and depreciation jointly diminish residual car values[cite: 2].
  * `Pojemność silnika` (engine displacement) demonstrates a weak-to-moderate positive correlation with price[cite: 1], as larger displacement engines are predominantly associated with higher-end or performance segments[cite: 1].
* **Powertrain Realities in the Secondary Market**: Despite growing interest in electromobility, internal combustion engines remain dominant—petrol engines account for **53.9%** and diesel for **33.3%** of all offerings[cite: 1]. Hybrids (**5.7%**) and LPG-converted vehicles (**5.5%**) maintain niche representation[cite: 1], while full battery electric vehicles (BEVs) remain marginal at just **1.4%**[cite: 1].
* **Balanced Transmission Preferences**: The market is evenly divided between manual (**50.3%**) and automatic (**49.7%**) transmissions[cite: 1], indicating a steady transition toward automatics even within the used vehicle segment.
* **Feature Engineering & Imputation Strategy**: Over **57%** of listings lacked explicit engine displacement entries[cite: 1]. Using regular expressions on the model titles combined with a 3-tier hierarchical median imputation (grouped by `Marka` + `Model`, then `Marka`, then global median) successfully recovered full sample coverage without biasing central tendencies[cite: 1, 2].

---

## 📂 Repository Structure

```plaintext
├── Data/
│   ├── agregator.py               # Script merging JSON files into a single CSV
│   ├── complete_data.csv          # Raw consolidated dataset (11,998 records)
│   └── cars_data.csv              # Cleaned & imputed dataset (ready for analysis)
├── EDA_data_proccessing.ipynb     # Notebook: data cleaning, imputation, visualization, and EDA
├── predictive_model.ipynb         # Notebook: OLS, log transformation, assumptions testing & evaluation
├── test.py                        # Web scraper (requests + BeautifulSoup4)
├── requirements.txt               # Environment dependencies
└── README.md                      # Project documentation
```
## 📊 Exploratory Data Analysis (EDA) Insights

Key automotive market patterns and findings identified during the analysis of the dataset:

### 1. Price Distribution & Skewness
* **Central Tendencies:** The mean car price in the dataset was approximately **77,317 PLN**, whereas the median stood at **47,000 PLN** (ranging from a minimum of 1,350 PLN to nearly 1.6 million PLN).
* **Market Concentration:** The majority of listings were clustered in the lower and middle price brackets (predominantly under 100,000 PLN).
* **Distribution Properties:** The `Price` variable exhibited strong positive (right-tail) skewness. This validated the necessity of applying a **logarithmic transformation** ($\ln(\text{Price})$) to achieve linearity and satisfy OLS homoscedasticity assumptions.

### 2. Vehicle Age & Local Environmental Regulations
* **Age Metrics:** The average production year was **2016** (median: 2017), with an average recorded mileage of approximately **142,000 km**.
* **Cohort Breakdown:** The vast majority of listed cars were manufactured after 2010. Vehicles built prior to 2004 represented a negligible fraction of the market, which can be linked to the planned implementation of the Clean Transport Zone (Strefa Czystego Transportu – SCT) in Kraków.
* **Depreciation & Mileage:** A strong negative linear correlation was observed between production year and mileage (older cars exhibit significantly higher odometer readings).

### 3. Feature Correlations with the Dependent Variable
* **Price vs. Year:** A moderate positive correlation — newer vehicles systematically command higher market valuations.
* **Price vs. Mileage:** A moderate negative correlation — market value depreciates with higher vehicle wear and tear.
* **Price vs. Displacement:** A weak-to-moderate positive correlation (larger engine displacements frequently align with premium or upper-tier segments).

### 4. Technical Characteristics & Market Structure
* **Powertrain Breakdown:** The market was dominated by petrol units (**53.9%**) and diesel engines (**33.3%**). Hybrids (**5.7%**) and LPG-equipped cars (**5.5%**) represented a minor share, while full battery electric vehicles (BEVs) remained a market margin at roughly **1.4%**.
* **Transmission Types:** Offerings were evenly distributed between manual (**50.3%**) and automatic (**49.7%**) gearboxes.
* **Brand Landscape:** The most represented brand was BMW (over 920 listings), with the BMW 3 Series being the single most common model in the dataset.

---

## 📈 Predictive Model (OLS Linear Regression)

### 1. Mathematical Specification
To account for exponential asset depreciation over time and address residual heteroscedasticity, an econometric **log-linear (semi-logarithmic)** model was implemented using Classical Ordinary Least Squares:

$$\ln(\text{Price}_i) = \beta_0 + \beta_1 \cdot \text{Year}_i + \beta_2 \cdot \text{Mileage}_i + \beta_3 \cdot \text{Displacement}_i + \sum_{k} \gamma_k D_{ki} + \varepsilon_i$$

Where:
* $\ln(\text{Price})$ — Natural logarithm of the car price in PLN (dependent variable).
* $\beta_1, \beta_2, \beta_3$ — Semi-elasticities for numerical variables (e.g., $100 \cdot \beta_1$ represents the estimated percentage change in vehicle price *ceteris paribus* for each 1-year increase in age).
* $D_{ki}$ — Dummy variables encoding categorical predictors (`Brand`, `Fuel`, `Transmission`).

### 2. Gauss-Markov Assumptions Verification
* **Linearity in Parameters:** Initial scatter plots revealed distinct non-linear dynamics between price, year, and mileage. The $\ln(\text{Price})$ transformation linearized these structural relationships.
* **Homoscedasticity:** Log-transforming the response variable stabilized error variance across the fitted value spectrum, mitigating fan-shaped residual heteroscedasticity.
* **No Autocorrelation of Residuals:** Given the cross-sectional nature of the data (a point-in-time snapshot of independent market listings), the assumption of zero serial autocorrelation holds *a priori*.

---

## 💻 Tech Stack & Requirements

* **Python Version:** $\ge 3.8$ (tested on Python 3.13)
* **Core Libraries:**
  * Data Manipulation: `pandas`, `numpy`
  * Econometrics & Machine Learning: `statsmodels`, `scikit-learn`
  * Visualization: `matplotlib`, `seaborn`
  * Web Scraping: `requests`, `beautifulsoup4`

Installation via pip:
```bash
pip install pandas numpy requests beautifulsoup4 seaborn matplotlib scikit-learn statsmodels
