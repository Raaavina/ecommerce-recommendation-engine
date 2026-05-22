# Step 1: Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container to /app
WORKDIR /app

# Step 3: Copy the requirements file into the container to install dependencies
COPY requirements.txt .

# Step 4: Install packages normally, but isolate xgboost to its lean CPU-only core
RUN pip install --no-cache-dir fastapi uvicorn pandas numpy scikit-learn seaborn matplotlib && \
    pip install --no-cache-dir xgboost --no-deps

# Step 5: Copy our application code and data directories into the container
COPY src/ ./src/
COPY data/ ./data/
COPY main.py .

# Step 6: Expose port 8000 for network communication
EXPOSE 8000

# Step 7: Define the command to run the FastAPI app using Uvicorn when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]