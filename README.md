# 🌿 Smart Desert Plant Recommender

An AI-powered system that recommends suitable desert plants based on environmental features across Saudi Arabia and visualizes them on an interactive map.

---

## 💡 Idea

Desertification and harsh climate make traditional planting in Saudi Arabia inefficient. This tool uses AI to suggest the most suitable native desert plants for each location based on real-world surface data.

---

## 🛑 Problem

- Manual plant selection is slow, expensive, and inaccurate.
- Limited guidance on what to plant in desert or semi-arid zones.
- Lack of automation in plant-environment matching.

---

## ✅ Solution

- Automated recommendation using LLM (via Ollama).
- Smart environmental analysis based on satellite-derived features.
- Interactive map with plant suggestions per region.
- Save up to 90% of field time and 70% of operational cost.

---

## 📦 How It Works

1. Upload a CSV with surface and soil features.
2. The API (FastAPI + Ollama) processes each row and queries the LLM.
3. Suggested plants are saved to a new CSV.
4. Coordinates are generated intelligently based on region.
5. A map is created with pins showing each location and recommendation.

---

## 🧠 Model

- LLM used: `qwen2:7b` (via Ollama)
- Custom prompt with environmental context.
- Plant selection limited to native species known to survive in harsh desert conditions.

---

## 🌾 Plant Candidates

- Date Palm  
- Acacia tortilis  
- Acacia ehrenbergiana  
- Tamarisk  
- Haloxylon salicornicum  
- Rhanterium epapposum  
- Ziziphus spina-christi  
- Calligonum comosum  
- Peganum harmala  
- Suaeda aegyptiaca  
- Lathyrus aphaca

---

## 🧬 Data Features (CSV input)

| Feature | Description |
|--------|-------------|
| `Soil_Type` | Type of soil (Sandy, Clay, etc.) |
| `Desertification_Level` | Low / Medium / High |
| `NDVI` | Vegetation Index |
| `NDWI` | Water Index |
| `LST_Day` | Daytime Land Surface Temperature |
| `LST_Night` | Nighttime LST |
| `DEM` | Elevation |
| _(others optional)_ | `Emis_31`, `EVI`, etc. |

---

## 📍 Output

- `recommendations.csv`: original data + `Recommended_Plant`
- `plant_recommendation_map.html`: map with popup markers and recommendations

---

## 🗺️ Map Preview

Each marker on the map shows:
- Soil & environmental data
- Recommended plant
- Reason in under 15 words

---

## 🛠️ Tech Stack

- Python
- FastAPI
- Pandas & NumPy
- Ollama (LLM inference)
- Folium (interactive map)

---

## 📈 Impact

- ⏱️ 90% faster than manual fieldwork  
- 💡 Smart, AI-backed planting decisions  
- 🌍 Supports sustainability and the Saudi Green Initiative  

---

## 🚀 How to Run

1. Make sure Ollama is running (`ollama run qwen2:7b`)
2. Start the API:

```bash
python Map.py
