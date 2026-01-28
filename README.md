# 🛡️ ShadowTrace AI: Autonomous Data Lineage & Audit Agent

**ShadowTrace AI** is an agentic framework designed to solve the "Shadow AI" problem—the unauthorized use of AI tools by employees that leads to data egress. It transforms massive, unstructured network logs into clear, diagnostic security reports using an autonomous reasoning loop.

---

## 📌 Project Overview

This project is an **End-to-End AI Security Framework** designed to ingest, process, and visualize high-volume network events in real-time. 

Built to simulate a production-grade security environment, the system handles "messy" lineage data, performs automated **Agentic Audits**, and serves actionable insights via a live interactive dashboard.

---

## 🏗️ Architecture

The pipeline follows a **Reasoning-Verification** architecture:

1. **Data Ingestion (Producer):** Processes high-cardinality data events (File movements, API calls) with intentional security anomalies to simulate production threats.
2. **Reasoning Loop (Agent):** An autonomous agent built with **LangGraph** traces data lineage to determine the "Why" behind potential breaches.
3. **Verification Layer (Guardrails):** Implemented via **Pydantic** to deterministicly validate AI findings against corporate policy before reporting.
4. **Analytics Layer (Dashboard):** Serves real-time risk gauges and downloadable PDF audit reports via **Streamlit**.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

---

## ⚙️ Installation & Setup

### **1. Prerequisites**
* Docker Desktop installed and running.
* Python 3.11+ (if running locally).

### **2. Using Docker (Recommended)**
Build and deploy the containerized service:

```powershell
# Build the image
docker build -t shadowtrace .

# Run the container
docker run -p 8501:8501 shadowtrace
```

> **Note:** Access the dashboard at: `http://localhost:8501`

### **3. Local Setup**

```bash
# Install dependencies
pip install -r requirements.txt
# Run the dashboard
streamlit run app.py
