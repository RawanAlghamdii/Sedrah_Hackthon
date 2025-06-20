from fastapi import FastAPI, UploadFile, File
import pandas as pd
import ollama
import uvicorn
import socket
import time
import io
import asyncio

app = FastAPI(title="🌿 Plant Recommender API")

@app.post("/recommend/")
async def recommend(file: UploadFile = File(...)):
    print("🔹 Starting recommend endpoint")
    try:
        contents = await file.read()
        print("🔹 File read successfully")
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        #df.drop(columns=["Latitude", "Longitude"], inplace=True)
        print(f"🔹 CSV loaded, shape: {df.shape}")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return {"error": "❌ Failed to read the CSV file", "details": str(e)}

    async def get_recommendation(row):
        prompt = f"""
You are an agricultural assistant AI.
Recommend the best plant to grow in this environment based on the following surface features:

- Soil Type: {row.get('Soil_Type', 'unknown')}
- Desertification Level: {row.get('Desertification_Level', 'unknown')}
- NDVI (Vegetation Index): {row.get('NDVI', 'unknown')}
- NDWI (Water Index): {row.get('NDWI', 'unknown')}
- Land Surface Temperature (Day): {row.get('LST_Day', 'unknown')}
- Elevation: {row.get('DEM', 'unknown')}

Consider only these plants for recommendation:
Date Palm, Tamarisk, Acacia tortilis, Acacia ehrenbergiana, Haloxylon salicornicum, 
Rhanterium epapposum, Ziziphus spina-christi, Calligonum comosum, Peganum harmala, 
Suaeda aegyptiaca, Lathyrus aphaca.

Give a plant name and short explain why it is suitable, less than 15 words.
"""

        print(f"🔹 Sending prompt for row index {row.name}")
        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model="qwen2:7b",
                messages=[
                    {"role": "system", "content": "You are a smart farming assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(f"🔹 Received response for row index {row.name}")
            return response['message']['content'].strip()
        except Exception as e:
            print(f"❌ Error in ollama.chat for row index {row.name}: {e}")
            return f"❌ Error getting recommendation: {e}"

    print("🔹 Starting to process rows concurrently")
    
    # خذ أول 1000 صف فقط
    df_subset = df.head(200).copy()

    # أنشئ المهام للتوصية على كل صف
    tasks = [get_recommendation(row) for _, row in df_subset.iterrows()]

    # نفّذ المهام كلها دفعة واحدة
    results = await asyncio.gather(*tasks)

    # خزّن النتائج في DataFrame جديد
    df_result = df_subset.copy()
    df_result["Recommended_Plant"] = results
    print("🔹 Added recommendations to dataframe")

    # حفظ النتائج في ملف CSV
    df_result.to_csv(r"C:\Users\96653\Downloads\recommendations.csv", index=False)
    print("🔹 Saved recommendations to recommendations.csv")

    # إعادة أول 5 صفوف كاستجابة API
    return df_result.head(5).to_dict(orient="records")


def check_ollama_ready(host='localhost', port=11434):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


if __name__ == "__main__":
    while not check_ollama_ready():
        print("🕒 Waiting for Ollama to start on port 11434...")
        time.sleep(3)

    print("✅ Ollama is ready. Pulling the model if needed...")
    ollama.pull("qwen2:7b")

    print("🚀 API running at http://127.0.0.1:8000/docs")
    uvicorn.run("sedrah:app", host="0.0.0.0", port=8000)
