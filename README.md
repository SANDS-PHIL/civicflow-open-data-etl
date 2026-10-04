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

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (Optional, for containerized run)

### Option 1: Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SANDS-PHIL/civicflow-open-data-etl.git
   cd civicflow-open-data-etl
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env to set your API_URL and FALLBACK_CSV paths
   ```

5. **Run the ETL Pipeline:**
   ```bash
   python main.py
   ```

6. **Launch the Dashboard:**
   ```bash
   streamlit run app.py
   ```

### Option 2: Docker Deployment

For a production-ready, containerized environment:

```bash
docker-compose up --build
```
*The dashboard will be available at `http://localhost:8501`.*

---

## ⚠️ Security & Usage Disclaimer

**IMPORTANT: This is a proof-of-concept for PUBLIC DATA ONLY.**

- **No Internal Data:** Do NOT use this pipeline with internal, confidential, or secure government systems without explicit authorization and a formal security review.
- **Not a Legal Document:** The generated LIM Summaries are for informational and workflow-acceleration purposes only. They do not replace official LIM reports issued under the Local Government Official Information and Meetings Act 1987.
- **Compliance:** Users are responsible for complying with all relevant data protection laws (e.g., NZ Privacy Act 2020) and open data licensing agreements.

---

## 🤝 Contributing & Ecosystem Partnership

CivicFlow is built as a digital public good. We welcome contributions, architectural reviews, and ecosystem partnerships from System Integrators, local government IT teams, and civic tech advocates.

For partnership inquiries or pro-bono architectural reviews, please contact the repository owner via LinkedIn or open an Issue.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
