import pickle
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'pricing_model.pkl')

def predict_final_price(sample_input: dict) -> float:
    with open(MODEL_PATH, 'rb') as f:
        pipeline = pickle.load(f)

    # print("✅ Loaded pipeline steps:", pipeline.named_steps)
    # print("✅ Loaded pipeline step keys:", list(pipeline.named_steps.keys()))

    df = pd.DataFrame([sample_input])
    print(f"🔍 Input to model: {df.columns.tolist()} | shape: {df.shape}")
    
    prediction = pipeline.predict(df)[0]
    return prediction
