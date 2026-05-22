# E-Commerce Hybrid Recommendation Engine Microservice

### 🚀 End-to-End Machine Learning Engineering Case Study & Project Charter

---

## 1. Project Charter & Business Context

### 🎯 Objective

To design, develop, and containerize a high-performance, real-time recommendation engine microservice. This service transitions an offline data science model into an isolated, scalable, production-ready REST API capable of serving personalized product recommendations to e-commerce customers instantly.

### 💼 The Business Problem

E-commerce platforms capture massive amounts of transactional data, but static storefronts fail to capitalize on historical user behavior. Without personalized recommendations, user engagement drops, average order value (AOV) stagnates, and conversion rates suffer.

- **The Goal:** Take raw historical transaction data and build an API endpoint that answers a single production question in milliseconds: _"Given `CustomerID X`, what 5 products are they most likely to buy next?"_

### 🛠️ Scope of Engineering Work

- **Phase 1: Exploratory Data Analysis (EDA):** Clean, preprocess, and validate behavioral patterns in historical data and synethesized data of clickstream and log activity to make dataset more robust (`notebook/01_eda.ipynb`).
- **Phase 2: Hybrid Modeling:** Implement collaborative filtering paired with an **XGBoost** ranking/scoring model pipeline (`notebook/02_model.ipynb` & `src/models.py`).
- **Phase 3: Production API Gateway:** Wrap the model inside an asynchronous **FastAPI** web application handling strict JSON payloads (`main.py`).
- **Phase 4: DevOps & Containerization:** Package the entire system code, data cache, and dependencies inside an optimized **Docker** container blueprint (`Dockerfile`).

---

## 2. Technical Decisions & "The Why"

As a production-grade machine learning system, every architectural choice was made to balance **system performance**, **resource efficiency**, and **environment reproducibility**.

### ⚡ Why FastAPI instead of Flask or Django?

- **Speed & Concurrency:** FastAPI is built on top of Starlette and Uvicorn, achieving benchmark speeds on par with NodeJS and Go. It handles concurrent requests asynchronously, which is vital for high-traffic web checkouts.
- **Data Validation:** It utilizes Pydantic under the hood. If an invalid or malicious `customer_id` type is passed, the API blocks it automatically and returns a clean error schema before hitting our model layer.
- **Auto-Documentation:** It natively hosts live, interactive Swagger documentation (`/docs`), significantly speeding up frontend-to-backend integration.

### 🐳 Why Docker Containerization?

The classic software problem is: _"It worked on the developer's laptop, but broke on the production server."_ - **Environment Isolation:** Python dependencies like `pandas` and `xgboost` rely heavily on compiled underlying C++ binaries. Docker freezes the exact operating system, Python runtime version (`3.9-slim`), and library tree into an unchanging blueprint.

- **Cloud Readiness:** A containerized application can be deployed instantly to **AWS (ECS/Fargate)** or **Azure (Container Apps)** without modifying a single line of code.

### 🧠 Production Tradeoffs & Edge-Case Engineering Solved

During development, we encountered and engineered solutions for two critical production challenges:

1. **Host Infrastructure Protection (Windows Storage Optimization):**
   - _Problem:_ Docker's default Windows Subsystem for Linux (WSL2) storage layer stores virtual disk files (`ext4.vhdx`) on the `C:\` drive. Our host `C:\` drive was low on space (under 15 GB free), creating a severe crash risk during image builds.
   - _Solution:_ We re-routed Docker’s internal engine layout, migrating its active storage volume safely over to the spacious `D:\` drive partition (`D:\DockerStorage`), safeguarding system memory stability.
2. **Container Image Minimization (Stripping GPU Bloat):**
   - _Problem:_ Standard installation of `xgboost` automatically fetches heavy, 300+ MB Nvidia CUDA graphic acceleration drivers (`nvidia-nccl-cu12`). In our container environment, we are executing inference exclusively on standard CPU clusters.
   - _Solution:_ We altered the build pipeline (`RUN pip install ... xgboost --no-deps`) to bypass these graphic card attachments entirely. This cut container network compilation times down drastically, eliminated network timeout corruption errors, and dramatically minimized the final deployment footprint.

---

## 3. Directory Layout & Codebase Structure

```text
ecommerce-recommendation-engine/
│
├── .github/workflows/             # Continuous Integration / Deployment hooks
├── data/                          # Clansed transactional data assets
├── env/                           # Local Python Virtual Environment isolated path
├── notebook/                      # Data Science Research & Validation Lab
│   ├── 01_eda.ipynb               # Data cleaning and behavioral analysis
│   └── 02_model.ipynb             # Model prototyping, training, and verification
├── src/                           # Modular Production Source Code
│   ├── __init__.py                # Package initialization marker
│   ├── data_processing.py         # Vectorization and feature engineering pipelines
│   └── models.py                  # Hybrid inference, scoring, and ranking engine
│
├── Dockerfile                     # CPU-Optimized production container recipe
├── main.py                        # FastAPI microservice application gateway
├── requirements.txt               # Locked software dependency configuration
└── README.md                      # Comprehensive Project Charter & Documentation
```
