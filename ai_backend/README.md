# AI Backend - ML Integration

## Overview
This AI backend uses machine learning-based scoring algorithms extracted from research in `fake_detector.py`.

## Scoring Algorithm

### Weighted Components
Based on ML research, the authenticity score uses the following weights:

- **Logo/Seal Match**: 40% (Most important indicator)
- **Layout Similarity**: 35% (Second most important)  
- **Signature Authenticity**: 25% (Derived from logo + layout)

### Signature Derivation Algorithm
The signature score is derived using an intelligent algorithm:

```python
if (logo_score >= 80%) AND (layout_score >= 80%):
    signature_score = 90-100%  # High integrity
else:
    signature_score = 40-70%   # Low integrity
```

This approach recognizes that authentic signatures correlate with authentic logos and layouts.

## Training Data

### Logo Data
Located in `Fake/images/logo_data/`:
- 9 institution classes
- 31 total logo images
- Institutions: Anna University, COURSERA, FORAGE, GOOGLE, MANIPAL, NPTEL, SRM, Amity, Jain

### Layout Data  
Located in `Fake/images/layout_data/`:
- 11 certificate layout samples
- Used for document structure analysis

## API Endpoints

### POST /api/analyze-certificate
Analyzes uploaded PDF certificate and returns:

```json
{
  "success": true,
  "analysis": {
    "authenticity_score": 85.5,
    "fraud_likelihood": "Very Low",
    "authenticity_level": "Highly Authentic",
    "confidence": "High",
    "score_breakdown": {
      "ocr_quality": 80.0,
      "layout_similarity": 85.0,
      "seal_match": 90.0,
      "signature_authenticity": 95.0
    },
    "weights_used": {
      "logo_weight": "40%",
      "layout_weight": "35%",
      "signature_weight": "25%"
    }
  }
}
```

## Future Enhancements

### TensorFlow Integration
The original `fake_detector.py` includes trained models:
- **Logo Detection**: MobileNetV2 (9 classes)
- **Layout Analysis**: VGG16 (binary classification)

To integrate:
1. Install TensorFlow: `pip install tensorflow`
2. Train models using data in `Fake/images/`
3. Save models as `.h5` files
4. Create `ml_inference.py` service
5. Update analyzers to use ML predictions

## Dependencies

Current (Lightweight):
```
Flask
flask-cors
PyPDF2
pdf2image
pytesseract
Pillow
python-dotenv
```

With TensorFlow (Full ML):
```
+ tensorflow
+ numpy (for ML operations)
+ opencv-python (for advanced CV)
```

## Running the Server

```bash
cd ai_backend
python app.py
```

Server runs on http://localhost:5000

## Testing

Test the health endpoint:
```bash
curl http://localhost:5000/api/health
```

Test certificate analysis:
```bash
curl -X POST http://localhost:5000/api/analyze-certificate \
  -F "file=@certificate.pdf"
```
