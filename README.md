# Analytics for ML Features Dashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

An interactive data science dashboard designed to analyze user behavior, model performance, and spending efficiency for a platform offering Machine Learning features. This tool provides actionable insights into how different license tiers interact with various ML models. You can visit the app at this link: https://analytics-for-ml.streamlit.app

---

## 📖 Project Overview
This project processes a complex dataset containing user activity logs, license types, and credit consumption. It transforms raw data into a visual story across five key dimensions:
* **Usage Metrics:** Tracking 1,866 unique users across various features.
* **Cost Efficiency:** Analyzing the `spent_amount` relative to `requests_cnt`.
* **License Segmentation:** Differentiating behaviors between Basic, Standard, Premium, and Enterprise tiers.
* **Temporal Trends:** Monitoring daily, weekly, and monthly growth.

---

## Key Modules

### 1. Overview & Dataset Exploration
Initial high-level summary of the ecosystem.
* **Metrics:** Quick view of Total Users, Average Requests, and Total Spent.
* **Distribution:** Histograms showing Feature and License frequency.
* **Heatmap:** Correlation between specific Features and ML Models.

### 2. Relation Exploration
Deep dive into the relationship between license tiers and model usage.
* **Box Plots:** Visualizing request count and unit spending variance per model.
* **Regression Analysis:** Scatter plots with OLS trendlines showing the linear relationship between activity and costs.

### 3. Trends Over Time
Analyzing how user engagement evolves.
* **Daily Correlation:** Monitoring the stability of the usage-based pricing model.
* **Weekly/Monthly Aggregates:** Identifying "Working Day" peaks vs. "Weekend" troughs.
* **Behavior Segments:** Area charts showing the shift in user types (e.g., Core Users vs. Free Users).

### 4. User Behaviour Analysis
Focusing on retention and engagement funnels.
* **Engagement Funnel:** Tracking users from initial app use to high-credit spending.
* **Retention:** Histogram of "Days Active" grouped by license type.
* **Power Users:** Identifying the top 5 contributors to platform revenue per license.

### 5. Strategic Summary & KPIs
A final synthesis of all data points.
* **KPI Expanders:** Organized view of Efficiency, Engagement, and Power Usage metrics.
* **Recommendations:** Concrete business advice based on data patterns.

---

## Key Business Insights

* **Model Dominance:** Models C and D are the platform's "workhorses," handling the majority of high-demand tasks (Feature 1 & 4).
* **Usage-Based Pricing:** A strong positive correlation ($r \approx 0.94$) proves that the spending model scales predictably with activity.
* **The "Power User" Effect:** A small minority of Premium users accounts for a disproportionate share of total spending.
* **Retention Link:** Higher-tier licenses (Premium/Enterprise) show a direct correlation with longer user lifespans.

---

## Tech Stack
* **Language:** Python 3.x
* **Data Handling:** `pandas`, `numpy`
* **Visualization:** `plotly.express`, `matplotlib`
* **Web Framework:** `streamlit`
* **UI Components:** `streamlit_option_menu`, `streamlit_lottie`

---

## Installation & Running

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/ml-features-analytics.git](https://github.com/your-username/ml-features-analytics.git)
   cd ml-features-analytics
