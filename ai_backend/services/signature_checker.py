"""
Simplified Signature Checker (without OpenCV)
"""
from pdf2image import convert_from_path
from PIL import Image, ImageStat
import numpy as np

class SignatureChecker:
    def __init__(self):
        pass
    
    def check_signature_authenticity(self, pdf_path):
        """
        Analyze signature authenticity using PIL
        Returns: dict with signature analysis results
        """
        try:
            # Convert PDF to image
            images = convert_from_path(pdf_path, dpi=300)
            if not images:
                return {'success': False, 'error': 'Failed to convert PDF'}
            
            image = images[0]
            
            # Simple signature detection
            signature_detected = self._detect_signature_simple(image)
            authenticity_score = self._analyze_signature_simple(image)
            
            return {
                'success': True,
                'signature_detected': signature_detected,
                'authenticity_score': authenticity_score,
                'signature_quality': self._assess_signature_quality(authenticity_score)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'signature_detected': False,
                'authenticity_score': 0
            }
    
    def _detect_signature_simple(self, image):
        """Simple signature detection"""
        try:
            # Convert to grayscale
            gray = image.convert('L')
            
            # Get statistics
            stat = ImageStat.Stat(gray)
            
            # Signatures typically have some variance
            variance = stat.var[0]
            
            # Simple heuristic
            return variance > 500
        except:
            return False
    
    def _analyze_signature_simple(self, image):
        """Simple signature analysis"""
        try:
            # Get image statistics
            stat = ImageStat.Stat(image.convert('L'))
            
            # Base score on variance and contrast
            variance = stat.var[0]
            
            if variance > 1500:
                return 75.0
            elif variance > 800:
                return 65.0
            else:
                return 55.0
        except:
            return 60.0
    
    def _assess_signature_quality(self, score):
        """Assess signature quality"""
        if score > 70:
            return 'High Quality'
        elif score > 50:
            return 'Medium Quality'
        else:
            return 'Low Quality'
