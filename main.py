# main.py
from fastapi import FastAPI, HTTPException
from src.data_processing import DataPipeline
from src.models import HybridRecommender

app = FastAPI(title="E-Commerce Predictive Personalization Engine", version="1.0.0")

# Initialize and bootstrap our production matrix structures on startup
try:
    pipeline = DataPipeline(data_dir="data")
    df_sales = pipeline.load_clean_data()
    user_matrix = pipeline.build_user_item_matrix(df_sales)
    recommender = HybridRecommender(user_matrix)
except Exception as e:
    print(f"Bootstrap warning: Local data assets not built yet. {e}")
    recommender = None

@app.get("/")
def read_root():
    return {"status": "online", "engine": "XGBoost/Collaborative-Hybrid"}

@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    if recommender is None:
        raise HTTPException(status_code=500, detail="Recommendation engine uninitialized.")
    
    predictions = recommender.get_candidates(target_user=customer_id)
    return {
        "customer_id": customer_id,
        "recommendations": predictions
    }