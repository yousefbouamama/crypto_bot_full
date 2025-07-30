from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "✅ البوت يعمل"}

@app.get("/subscriptions")
def get_subscriptions():
    try:
        with open("subscriptions.json", "r") as f:
            data = json.load(f)
        return data
    except:
        return {"error": "لا يوجد اشتراكات"}
