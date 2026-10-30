# Contributing to CropGuard

Thank you for your interest in contributing to **CropGuard: an open-source crop disease and pest detection tool**! This project is aimed at assisting smallholder farmers, plant pathologists, and agricultural extension officers across India in early crop disease diagnosis and Integrated Pest Management (IPM).

---

## 🌾 Guidelines for Contribution

### 1. Code Standards
- **Python 3.10+**: Follow PEP 8 style guidelines.
- **Type Hinting**: Provide function type hints and comprehensive docstrings for algorithms (especially in `model.py`, `weather.py`, and `db.py`).
- **Safety First**: Never hardcode or invent pesticide dosages in `advisory.json`. All agricultural guidance must adhere strictly to ICAR (Indian Council of Agricultural Research), Central Insecticide Board & Registration Committee (CIBRC), and State Agriculture Extension principles.

### 2. Submitting Pull Requests
1. Fork the repository.
2. Create a descriptive feature branch:
   ```bash
   git checkout -b feature/new-crop-pathology
   ```
3. Test your changes locally:
   ```bash
   streamlit run app.py
   ```
4. Verify database migrations in `db.py` if changing schema.
5. Commit your changes with clear messages:
   ```bash
   git commit -m "feat(advisory): add chili leaf curl IPM protocols in Marathi and Hindi"
   ```
6. Push to your branch and open a Pull Request.

---

## 🔬 Testing New Disease Models
When introducing new Hugging Face models:
- Verify that inference runs smoothly on CPU instances.
- Map the output class labels in `model.py`'s `LABEL_MAPPING` dictionary.
- Add corresponding IPM entries in `advisory.json` across all three languages (English, Hindi, and Marathi).

---

## 📜 Code of Conduct
We are committed to providing a welcoming, inclusive, and harassment-free environment for all contributors. Respectful collaboration is expected at all times.
