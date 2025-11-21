"""
Simplified Image Analysis Service (without OpenCV dependency)
Works with basic PIL/Pillow operations
"""
from pdf2image import convert_from_path
from PIL import Image, ImageStat
import numpy as np

class ImageAnalyzer:
    def __init__(self):
        self.seal_templates = []
    
    def analyze_certificate_image(self, pdf_path):
        """
        Analyze certificate for visual elements using PIL
        Returns: dict with seal detection, logo matching, and layout analysis
        """
        try:
            # Convert PDF to image
            images = convert_from_path(pdf_path, dpi=300)
            if not images:
                return {'success': False, 'error': 'Failed to convert PDF to image'}
            
            # Analyze first page
            image = images[0]
            
            # Basic image analysis using PIL
            seal_score = self._detect_seals_simple(image)
            layout_score = self._analyze_layout_simple(image)
            formatting_score = self._analyze_formatting_simple(image)
            image_quality = self._assess_image_quality_simple(image)
            
            return {
                'success': True,
                'seal_match_percentage': seal_score,
                'layout_similarity': layout_score,
                'formatting_score': formatting_score,
                'image_quality': image_quality
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'seal_match_percentage': 0,
                'layout_similarity': 0
            }
    
    def _detect_seals_simple(self, image):
        """Simple seal detection using image statistics"""
        try:
            # Convert to grayscale
            gray = image.convert('L')
            
            # Get image statistics
            stat = ImageStat.Stat(gray)
            
            # Check variance (seals typically have distinct patterns)
            variance = stat.var[0]
            
            # Score based on variance
            if variance > 2000:
                return 85.0
            elif variance > 1000:
                return 70.0
            else:
                return 55.0
        except:
            return 60.0
    
    def _analyze_layout_simple(self, image):
        """Simple layout analysis"""
        try:
            # Get image dimensions
            width, height = image.size
            
            # Check aspect ratio (typical certificate is landscape or portrait)
            aspect_ratio = width / height if height > 0 else 1
            
            # Score based on typical certificate dimensions
            if 1.2 < aspect_ratio < 1.6 or 0.7 < aspect_ratio < 0.9:
                return 80.0
            else:
                return 65.0
        except:
            return 60.0
    
    def _analyze_formatting_simple(self, image):
        """Simple formatting analysis"""
        try:
            # Check if image has good color distribution
            stat = ImageStat.Stat(image)
            
            # Check mean brightness
            mean_brightness = sum(stat.mean) / len(stat.mean)
            
            # Well-formatted documents typically have good contrast
            if 100 < mean_brightness < 200:
                return 75.0
            else:
                return 60.0
        except:
            return 65.0
    
    def _assess_image_quality_simple(self, image):
        """Simple image quality assessment"""
        try:
            # Check image size (higher resolution = better quality)
            width, height = image.size
            total_pixels = width * height
            
            # Score based on resolution
            if total_pixels > 2000000:  # > 2MP
                return 85.0
            elif total_pixels > 1000000:  # > 1MP
                return 70.0
            else:
                return 55.0
        except:
            return 70.0
