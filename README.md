# SafeSeal - AI-Powered Academic Credentials Platform

## Setup Instructions

### Prerequisites
- Node.js (v18+)
- Python (v3.8+)
- Tesseract OCR

### 1. Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR`
3. Add to PATH or update path in `ai_backend/services/ocr_service.py`

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Install Python Dependencies

```bash
cd ai_backend
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cd ai_backend
copy .env.example .env
```

### 4. Start the AI Backend

```bash
cd ai_backend
python app.py
```

The AI backend will start on http://localhost:5000

### 5. Start the Next.js Frontend

```bash
cd client
npm run dev
```

The frontend will start on http://localhost:3000

Images
<img width="1919" height="944" alt="Screenshot 2025-11-21 232700" src="https://github.com/user-attachments/assets/a32bc985-573e-477b-a095-08548cedd11a" />
<img width="1043" height="647" alt="Screenshot 2025-11-21 232719" src="https://github.com/user-attachments/assets/7cf9cf04-6f0a-4c0d-96d9-7095b220abe8" />
<img width="1919" height="936" alt="Screenshot 2025-11-21 232735" src="https://github.com/user-attachments/assets/333a50ea-a3cd-4ca5-9f47-aa8d1ba1978a" />

## Features

### 🔐 Blockchain Certificate Management
- **Issue Certificate**: Create and issue academic credentials on the blockchain
- **Verify Certificate**: Verify authenticity using blockchain hash
- **Revoke Certificate**: Revoke previously issued certificates

### 🤖 AI Authenticity Check
Upload a PDF certificate for comprehensive AI analysis:

1. **OCR Text Extraction** - Extract and parse certificate data
2. **Layout Analysis** - Compare document structure with official templates
3. **Seal/Logo Detection** - Detect and match institutional seals
4. **Signature Verification** - Analyze signature authenticity
5. **Fraud Detection** - Calculate overall authenticity score (0-100%)

## API Endpoints

### AI Backend (Port 5000)
- `GET /api/health` - Health check
- `GET /api/test` - Test endpoint
- `POST /api/analyze-certificate` - Analyze PDF certificate (multipart/form-data)

## Project Structure

```
Academic Cerdentials/
├── ai_backend/              # Python AI service
│   ├── services/           # AI analysis services
│   │   ├── ocr_service.py
│   │   ├── image_analyzer.py
│   │   ├── signature_checker.py
│   │   ├── layout_analyzer.py
│   │   └── scoring_engine.py
│   ├── uploads/            # Temporary PDF storage
│   ├── app.py             # Flask API server
│   └── requirements.txt
├── client/                 # Next.js frontend
│   └── src/
│       └── app/
│           ├── ai-verify/  # AI verification page
│           ├── issue/      # Issue certificate page
│           ├── verify/     # Blockchain verify page
│           └── revoke/     # Revoke certificate page
└── smart_contracts/        # Hardhat blockchain
    └── contracts/
        └── CertificateRegistry.sol
```

## Usage

1. **Navigate to http://localhost:3000**
2. **Click "AI Authenticity Check"**
3. **Upload a PDF certificate**
4. **Click "Analyze with AI"**
5. **View comprehensive authenticity report**

## Technologies

- **Frontend**: Next.js 16, React 19, TypeScript
- **Blockchain**: Hardhat, Solidity, Ethers.js
- **AI Backend**: Python, Flask, OpenCV, Tesseract OCR
- **Image Processing**: pdf2image, Pillow, NumPy
