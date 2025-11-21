"""
Simplified Layout Analyzer (without OpenCV)
"""
from pdf2image import convert_from_path
from PIL import Image, ImageStat, ImageFilter
import numpy as np

class LayoutAnalyzer:
    def __init__(self):
        self.reference_layouts = []
    
    def analyze_layout(self, pdf_path):
        """
        Analyze document layout using PIL
        Returns: dict with layout analysis results
        """
        try:
            # Convert PDF to image
            images = convert_from_path(pdf_path, dpi=300)
            if not images:
                return {'success': False, 'error': 'Failed to convert PDF'}
            
            image = images[0]
            
            # Analyze layout
            structure_score = self._analyze_structure_simple(image)
            alignment_score = self._check_alignment_simple(image)
            anomalies = self._detect_anomalies_simple(image)
            
            overall_score = (structure_score + alignment_score) / 2
            
            return {
                'success': True,
                'layout_similarity': overall_score,
                'structure_score': structure_score,
                'alignment_score': alignment_score,
                'anomalies_detected': len(anomalies),
                'anomalies': anomalies
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'layout_similarity': 0
            }
    
    def _analyze_structure_simple(self, image):
        """Simple structure analysis"""
        try:
            # Get image statistics
            stat = ImageStat.Stat(image.convert('L'))
            
            # Check variance (well-structured docs have good variance)
            variance = stat.var[0]
            
            if variance > 1500:
                return 80.0
            elif variance > 800:
                return 65.0
            else:
                return 55.0
        except:
            return 60.0
    
    def _check_alignment_simple(self, image):
        """Simple alignment check"""
        try:
            # Apply edge detection using PIL
            edges = image.convert('L').filter(ImageFilter.FIND_EDGES)
            
            # Get statistics of edges
            stat = ImageStat.Stat(edges)
            edge_density = sum(stat.mean) / len(stat.mean)
            
            # Score based on edge density
            if edge_density > 30:
                return 75.0
            elif edge_density > 15:
                return 65.0
            else:
                return 55.0
        except:
            return 65.0
    
    def _detect_anomalies_simple(self, image):
        """Simple anomaly detection"""
        anomalies = []
        
        try:
            # Check image quality
            stat = ImageStat.Stat(image.convert('L'))
            variance = stat.var[0]
            
            if variance < 500:
                anomalies.append('Low image quality or blur detected')
            
            # Check aspect ratio
            width, height = image.size
            aspect_ratio = width / height if height > 0 else 1
            
            if aspect_ratio < 0.5 or aspect_ratio > 2.5:
                anomalies.append('Unusual document dimensions detected')
        except:
            pass
        
        return anomalies
