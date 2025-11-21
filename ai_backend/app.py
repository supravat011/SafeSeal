"""
Flask API Server for AI Certificate Analysis
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

# Import services
from services.ocr_service import OCRService
from services.image_analyzer import ImageAnalyzer
from services.signature_checker import SignatureChecker
from services.layout_analyzer import LayoutAnalyzer
from services.scoring_engine import ScoringEngine

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=[os.getenv('CORS_ORIGINS', 'http://localhost:3000')])

# Configuration
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max
ALLOWED_EXTENSIONS = {'pdf'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
ocr_service = OCRService()
image_analyzer = ImageAnalyzer()
signature_checker = SignatureChecker()
layout_analyzer = LayoutAnalyzer()
scoring_engine = ScoringEngine()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Backend is running'}), 200

@app.route('/api/analyze-certificate', methods=['POST'])
def analyze_certificate():
    """
    Main endpoint for certificate analysis
    Accepts PDF file and returns comprehensive AI analysis
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Perform AI analysis
        try:
            # OCR Analysis
            ocr_results = ocr_service.extract_text_from_pdf(filepath)
            
            # Image Analysis
            image_results = image_analyzer.analyze_certificate_image(filepath)
            
            # Signature Analysis
            signature_results = signature_checker.check_signature_authenticity(filepath)
            
            # Layout Analysis
            layout_results = layout_analyzer.analyze_layout(filepath)
            
            # Combine all results
            analysis_results = {
                'ocr': ocr_results,
                'image': image_results,
                'signature': signature_results,
                'layout': layout_results
            }
            
            # Calculate final authenticity score
            final_score = scoring_engine.calculate_authenticity_score(analysis_results)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Return comprehensive results
            return jsonify({
                'success': True,
                'filename': filename,
                'analysis': {
                    'authenticity_score': final_score['final_score'],
                    'fraud_likelihood': final_score['fraud_likelihood'],
                    'authenticity_level': final_score['authenticity_level'],
                    'confidence': final_score['confidence'],
                    'score_breakdown': final_score['score_breakdown'],
                    'ocr_data': {
                        'extracted_text': ocr_results.get('text', '')[:500],  # First 500 chars
                        'word_count': ocr_results.get('word_count', 0),
                        'extracted_fields': ocr_results.get('extracted_data', {})
                    },
                    'visual_analysis': {
                        'seal_match_percentage': image_results.get('seal_match_percentage', 0),
                        'layout_similarity': layout_results.get('layout_similarity', 0),
                        'formatting_score': image_results.get('formatting_score', 0),
                        'image_quality': image_results.get('image_quality', 0)
                    },
                    'signature_analysis': {
                        'signature_detected': signature_results.get('signature_detected', False),
                        'authenticity_score': signature_results.get('authenticity_score', 0),
                        'signature_quality': signature_results.get('signature_quality', 'Unknown')
                    },
                    'layout_details': {
                        'structure_score': layout_results.get('structure_score', 0),
                        'alignment_score': layout_results.get('alignment_score', 0),
                        'anomalies_detected': layout_results.get('anomalies_detected', 0),
                        'anomalies': layout_results.get('anomalies', [])
                    }
                }
            }), 200
            
        except Exception as analysis_error:
            # Clean up file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            
            return jsonify({
                'success': False,
                'error': f'Analysis failed: {str(analysis_error)}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        'message': 'AI Backend API is working!',
        'endpoints': {
            'health': '/api/health',
            'analyze': '/api/analyze-certificate (POST with PDF file)'
        }
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print(f"🚀 AI Backend starting on port {port}")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🔧 Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
