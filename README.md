# Medical Consultation Platform — Financial Analysis (snapshot)

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-View%20Charts-27AE60?style=for-the-badge)](https://dmitriifed.github.io/medical-platform-financial-analysis/)

An end-to-end financial analysis of an online medical consultation platform. The project covers the full pipeline — from raw CRM data to an interactive multi-topic dashboard — and produces actionable business insights across revenue, pricing, cost, margin, doctor economics, and patient retention.

> **Snapshot note:** This is a portfolio snapshot. All financial values are scaled and all IDs are anonymised. Data structure, distributions, and analytical conclusions reflect the real project.

---

## Key Findings at a Glance

![Key findings at a glance](docs/findings_at_a_glance.png)

1. **Revenue grows, but gross margin is shrinking** → growth is volume-driven; fix unit economics before scaling further
2. **Video consultations out-earn chat** → higher profit per consultation; shift the service mix toward video
3. **Cancellations are rising over time** → a growing, recoverable revenue leak; add reminders and sync availability
4. **A small group of doctors drives most revenue** → concentration risk; broaden and activate the provider base
5. **Patients rarely return after the first visit** → lifetime value is capped; retention is the biggest untapped lever
6. **Four specialties generate most gross profit** → endocrinology, general medicine, surgery, cardiology; scale supply here

Full write-up: [`reports/executive_summary.md`](reports/executive_summary.md) · [`reports/key_findings.md`](reports/key_findings.md) · [`reports/recommendations.md`](reports/recommendations.md)

---

## Live Dashboard

**[→ Open interactive dashboard](https://dmitriifed.github.io/medical-platform-financial-analysis/)**

26 Plotly charts across 8 topics. No installation required — opens in any browser.

---

## What This Project Demonstrates

**Python & Data Engineering**
- Multi-source data pipeline: CRM exports + daily FX rates + hierarchy lookups
- EUR normalisation across RUB / USD / ILS / USDT payment currencies
- Automated notebook execution via `run_viz.py` — no Jupyter required to regenerate output
- Parameterised outlier clipping, specialty joins, cohort construction

**Financial & Business Analysis**
- Revenue vs gross margin divergence — identifying unit economics deterioration
- Service mix analysis (Video vs Chat) with profitability breakdown
- Cancellation impact: revenue foregone quantification and doctor-level rates
- Pareto analysis for both doctors and patients (revenue concentration)
- Doctor specialty profitability: GP treemap, grouped bars, monthly dynamics
- Patient cohort retention matrix (monthly cohorts, 12-month window)

---

## Analysis Topics

| Topic | Charts | Key Question |
|---|---|---|
| 0 — Business Overview | 3 | Is the business growing efficiently? |
| 1 — Revenue Analysis | 2 | What drives revenue mix? |
| 2 — Pricing Analysis | 2 | How do Video and Chat prices differ? |
| 3 — Volume & Cancellation | 3 | How much revenue is being lost to cancellations? |
| 4 — Cost Analysis | 3 | What does doctor compensation look like? |
| 5 — Margin Analysis | 2 | Which services are most profitable? |
| 7 — Doctor Economics | 8 | Who generates value, and how is it distributed? |
| 8 — Patient Economics | 3 | Do patients return? |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/dmitriifed/medical-platform-financial-analysis.git
cd medical-platform-financial-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate dashboard
python notebooks/run_viz.py
# → opens visualisations/quick_viz_4.html in your browser
```

---

## Project Structure

```
medical-platform-financial-analysis/
├── data/
│   ├── processed/              # Scrambled CRM data (pipeline output)
│   └── raw/hierarchy/          # Specialty grouping lookups
├── notebooks/
│   ├── quick_viz_4.ipynb       # Main analysis notebook (25 active charts)
│   └── run_viz.py              # Runs notebook → exports HTML dashboard
├── reports/
│   ├── executive_summary.md
│   ├── key_findings.md
│   └── recommendations.md
├── docs/
│   ├── index.html              # GitHub Pages source (live dashboard)
│   └── findings_at_a_glance.png
├── requirements.txt
└── README.md
```

---

## Contributors

- [@dmitriifed](https://github.com/dmitriifed)
- [@sergey-berezovka](https://github.com/sergey-berezovka)
