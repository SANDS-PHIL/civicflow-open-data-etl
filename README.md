#  CivicFlow: Enterprise Open Data ETL & LIM-Lite Dashboard

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-005571.svg)](https://docs.pydantic.dev/)

**CivicFlow** is an open-source, MIT-licensed data aggregation and validation framework designed specifically for New Zealand local government. It automates the extraction, transformation, and loading (ETL) of public open data, providing a resilient, auditable, and interactive platform for urban planning and LIM (Land Information Memorandum) report workflows.

## 🎯 Purpose & Strategic Alignment

Designed to help local councils (e.g., Wellington City Council) automate and validate public open data pipelines. CivicFlow directly addresses operational inefficiencies highlighted in strategic reviews (such as WCC's *Future Fit Pōneke* report) by:
- Reducing manual data cross-referencing across fragmented legacy systems.
- Enforcing strict data governance and geospatial validation.
- Providing a zero-license-fee, agile alternative to traditional enterprise software rollouts.

## ✨ Key Features (v1.0)

### 🛡️ Enterprise Data Governance
- **Strict Validation:** Pydantic v2 models enforce NZ geospatial bounds and schema rules, preventing "garbage-in, garbage-out" scenarios.
- **Graceful Degradation:** Automatically falls back to a secure local cache if public APIs timeout or fail, ensuring zero downtime for downstream users.
- **Auditability:** Built-in Data Lineage and Observability tracking.

### 📊 Interactive LIM-Lite Dashboard
- **Spatial Analytics:** Interactive PyDeck map visualizing District Plan overlays and demographic data.
- **Workflow Automation:** One-click generation of branded LIM Summary PDFs for specific properties.
- **Data Export:** Real-time filtering and CSV export capabilities for council staff.

### 🐳 Container-Ready Deployment
- Fully supported via **Docker** and **Docker Compose** for secure, reproducible deployment in council environments.

## 🏗️ Architecture

```text
.
── app.py                  # Streamlit Dashboard (UI/UX)
├── main.py                 # ETL Pipeline Orchestrator
├── src/
│   ├── models.py           # Pydantic Data Models & Validation
│   ├── extract.py          # API Extraction & Fallback Logic
│   ├── transform.py        # Data Aggregation & Cleaning
│   └── load.py             # Database/CSV Loading
├── tests/                  # Pytest Unit Tests
├── Dockerfile              # Containerization config
└── docker-compose.yml      # Multi-container orchestration
```
