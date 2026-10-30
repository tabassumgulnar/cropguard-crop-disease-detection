# 🌱 CropGuard: Early Detection of Crop Diseases & Pests
**CropGuard: An Open-Source Crop Disease and Pest Detection Tool**  
**Author:** Tabassum Gulnar

CropGuard is an end-to-end, runnable agro-informatics and plant pathology platform designed to assist smallholder farmers and agriculture extension officers in detecting foliar crop diseases and insect pests early. It bridges deep learning vision models, real-time agro-meteorology, trilingual Integrated Pest Management (IPM), and spatial epidemiology into an accessible web application.

---

## 📌 Overview & Context
Foliar diseases (such as Early Blight, Late Blight, Bacterial Blight, and Purple Blotch) and vector-transmitted viral pathogens cause catastrophic yield losses across India, particularly in cash and staple crops like **Tomato**, **Cotton**, and **Onion**. 

Key challenges faced on the ground:
1. **Misdiagnosis & Calendar Spraying:** Farmers frequently misidentify fungal lesions as nutrient deficiencies or apply excessive, broad-spectrum chemical fungicides prophylactically without exceeding Economic Threshold Levels (ETL).
2. **Weather-Driven Epidemics:** High relative humidity (>75%), unseasonal rainfall, and warm temperatures create explosive incubation windows for sporulation that are rarely forecasted at the farm level.
3. **Language Barriers:** Scientific advisories from ICAR and State Agricultural Universities are often published in technical English, inaccessible to non-English speaking growers.
4. **Lack of Ground-Truth Surveillance:** District Agriculture Officers and Krishi Vigyan Kendras (KVKs) lack real-time digital surveillance maps to track localized infection clusters before regional outbreaks emerge.

CropGuard resolves these bottlenecks through an integrated diagnostic pipeline with strict safeguard thresholds and human-in-the-loop expert validation.

---

## 🏛️ System Architecture

```
                                  [ FARMER EDGE INTERFACE ]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
         Leaf Photo (Upload/Camera)                           Field GPS / Location
                      │                                               │
                      ▼                                               ▼
     [ Hugging Face Vision Pipeline ]                      [ Open-Meteo Weather API ]
   (MobileNet / ViT on PlantVillage)                      (Temp, Humidity, Rain, Wind)
                      │                                               │
                      ▼ Top-3 Confidences                             ▼
        ┌───────────────────────────┐                 [ Rule-Based Epidemiological Engine ]
        │ Confidence Gate:          │                 (Fungal Incubation & Vector Risk:    │
        │ < 60%  ──▶ UNCERTAIN FLAG │                  Low / Medium / High)                │
        │ ≥ 60%  ──▶ DIAGNOSIS      │                                 │
        └─────────────┬─────────────┘                                 │
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                                 [ SQLite DB: cropguard.db ]
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
        [ Trilingual IPM Advisory ]                      [ Officer Surveillance Dashboard ]
     (Cultural, Biological, Chemical,                 (Folium Pins + Hotspot HeatMaps,
        Safety in EN, HI, MR)                         Audit Log, Human-in-the-Loop Re-labeling)
```

---

## ✨ Core Features

### 1. Farmer Diagnostic Portal (`pages/1_🌾_Farmer_Diagnosis.py`)
- **Input Channels:** Upload leaf photos, live camera capture, or 1-click synthetic pathological samples.
- **Crop Support:** Tomato (`Solanum lycopersicum`), Cotton (`Gossypium hirsutum`), Onion (`Allium cepa`).
- **Precision AI Inference:** Pretrained Hugging Face Vision Transformers / MobileNets fine-tuned on plant pathology datasets, returning top-3 candidate diagnoses with percentage probabilities.
- **60% Confidence Safety Gate:** If top model confidence is `< 60%`, CropGuard suppresses automated chemical diagnoses and presents:
  > *"⚠️ Uncertain – please consult an agriculture officer"*  
  alongside photo retake tips, automatically logging the case for Taluka/District officer triage.

### 2. Live Weather Risk Assessment (`weather.py`)
- Queries Open-Meteo's open endpoint (zero API key needed) for temperature, relative humidity, precipitation, and wind velocity.
- Agro-meteorological rule engine calculates fungal spore proliferation risks:
  - **High Risk:** Relative humidity $\ge 85\%$ or $\ge 75\%$ with rainfall $> 0.5\text{ mm}$ at $18^\circ\text{C} - 28^\circ\text{C}$.
  - **Medium Risk:** Moderate humidity ($60\% - 75\%$) or warm, dry spells fostering sucking pest (whitefly/thrip) reproduction.
  - **Low Risk:** Sub-optimal temperatures or low ambient moisture suppressing sporulation.

### 3. Trilingual IPM Advisory Engine (`advisory.json` & `pages/3_📚_Disease_Advisory.py`)
- Standardized Integrated Pest Management (IPM) guidelines across **10+ common diseases**.
- Available in **English**, **हिन्दी (Hindi)**, and **मराठी (Marathi)**.
- Formatted in 4 scientific tiers:
  1. **🌱 Cultural Practices:** Crop spacing, drip irrigation, crop rotation, trap cropping, field sanitation.
  2. **🧫 Biological Controls:** *Trichoderma viride*, *Pseudomonas fluorescens*, *Chrysoperla*, *Beauveria bassiana*, neem formulations (NSKE 5%).
  3. **🧪 Chemical Controls (Strictly As Last Resort):** Follows Economic Threshold Levels (ETL); zero manufactured dosages; directs users to local ICAR/KVK notifications.
  4. **🦺 Operator Safety & Pre-Harvest Intervals (PHI):** Protective equipment and post-spray harvest intervals.

### 4. Agriculture Officer GIS Surveillance Dashboard (`pages/2_🛡️_Officer_Dashboard.py`)
- **Interactive Folium GIS Map:** Displays disease incident markers color-coded by severity, clickable popup diagnostics, and an aggregate epidemiological HeatMap layer.
- **Pre-populated Demo Dataset:** Includes 32 realistic agricultural reports across Maharashtra (Pune, Nashik, Jalgaon, Ahmednagar, Solapur, Nagpur, etc.).
- **Incident Audit Log:** Searchable and filterable data table with instant CSV export.
- **Human-in-the-Loop "Confirm / Correct Label" Tool:** Extension officers can confirm AI diagnoses or correct mislabeled cases, adding field notes that update the SQLite database for active learning pipelines.

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.10+
- `pip` package manager

### Installation
```bash
# 1. Clone repository
git clone https://github.com/cropguard/cropguard.git
cd cropguard

# 2. (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate demo samples and seed database (automatic on first run)
python3 generate_samples.py

# 5. Launch CropGuard Streamlit Application
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501` (or port 3000 if configured).

---

## 📁 Repository Structure
```
├── app.py                         # Main Streamlit hub, statistics, and system architecture
├── pages/
│   ├── 1_🌾_Farmer_Diagnosis.py   # Farmer leaf diagnosis, weather risk, & IPM advice
│   ├── 2_🛡️_Officer_Dashboard.py  # Officer Folium map, heatmaps, & active learning
│   └── 3_📚_Disease_Advisory.py   # Trilingual IPM catalog (EN, HI, MR)
├── advisory.json                  # Tri-lingual IPM database for 10+ diseases
├── model.py                       # Hugging Face Vision Transformer & agro-heuristic fallback
├── weather.py                     # Open-Meteo real-time weather & epidemiological risk
├── db.py                          # SQLite persistent storage & Maharashtra demo dataset
├── generate_samples.py            # Generates synthetic test leaf images in samples/
├── samples/                       # Pre-created test leaf images
├── requirements.txt               # Pinned Python package dependencies
├── README.md                      # Complete system documentation
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution and code of conduct guidelines
└── .gitignore                     # Git ignore rules
```

---

## ⚠️ Limitations
1. **Single Leaf vs Canopy View:** Diagnosis is performed on individual leaves; whole-field canopy context or root-level wilting (e.g. Fusarium wilt) requires multi-angle sampling.
2. **Connectivity Constraints:** Hugging Face model weight downloads require initial network bandwidth (~80MB); CropGuard includes a computer-vision heuristic fallback when operating completely offline.
3. **No Chemical Dosages:** By design, CropGuard does not prescribe specific chemical milliliter or gram quantities, as registered concentrations vary by brand formulation and soil characteristics.

---

## 🔮 Future Work
1. **IoT Sensor Mesh Integration:** Ingest live soil moisture, leaf wetness sensors, and ambient temperature from field micro-weather stations via MQTT/LoRaWAN.
2. **Active Learning Retraining Loop:** Automated retraining pipelines that incorporate verified and corrected labels from Agriculture Officers to fine-tune specialized vision models for regional crop varieties.
3. **Offline Progressive Web App (PWA) & Edge TFLite/ONNX:** Compiling model backbones into quantized ONNX or TensorFlow Lite formats for 100% offline edge inference on low-cost Android smartphones in remote villages without mobile coverage.
4. **Multispectral & Drone (UAV) Ingestion:** Orthomosaic stitching of NDVI/NDRE drone imagery for hectare-level early blight cluster detection before visual symptoms appear to the human eye.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
