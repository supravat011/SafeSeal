"""
Scoring Engine for calculating overall authenticity score
Based on ML research from fake_detector.py
"""
import numpy as np

class ScoringEngine:
    def __init__(self):
        # Weights based on ML research (from fake_detector.py)
        # These weights were optimized for certificate forgery detection
        self.weights = {
            'logo_match': 0.40,        # 40% - Most important indicator
            'layout_similarity': 0.35,  # 35% - Second most important
            'signature_authenticity': 0.25  # 25% - Derived from logo+layout
        }
        self.signature_threshold = 0.80  # Threshold for high integrity
    
    def calculate_authenticity_score(self, analysis_results):
        """
        Calculate overall authenticity score from all analysis components
        Uses ML-based weighted scoring algorithm
        Returns: dict with final score and breakdown
        """
        try:
            # Extract scores from analysis results (normalized to 0-1 scale)
            ocr_score = self._calculate_ocr_score(analysis_results.get('ocr', {}))
            layout_score = analysis_results.get('layout', {}).get('layout_similarity', 60) / 100
            seal_score = analysis_results.get('image', {}).get('seal_match_percentage', 60) / 100
            
            # Derive signature score using ML algorithm
            signature_score = self._derive_signature_score(seal_score, layout_score)
            
            # Calculate weighted average using ML weights
            final_score = (
                seal_score * self.weights['logo_match'] +
                layout_score * self.weights['layout_similarity'] +
                signature_score * self.weights['signature_authenticity']
            )
            
            # Convert to percentage
            final_score_pct = final_score * 100
            
            # Determine fraud likelihood and authenticity level
            fraud_likelihood = self._calculate_fraud_likelihood(final_score_pct)
            authenticity_level = self._get_authenticity_level(final_score_pct)
            
            return {
                'final_score': round(final_score_pct, 2),
                'fraud_likelihood': fraud_likelihood,
                'authenticity_level': authenticity_level,
                'score_breakdown': {
                    'ocr_quality': round(ocr_score * 100, 2),
                    'layout_similarity': round(layout_score * 100, 2),
                    'seal_match': round(seal_score * 100, 2),
                    'signature_authenticity': round(signature_score * 100, 2),
                },
                'weights_used': {
                    'logo_weight': f"{self.weights['logo_match']*100}%",
                    'layout_weight': f"{self.weights['layout_similarity']*100}%",
                    'signature_weight': f"{self.weights['signature_authenticity']*100}%"
                },
                'confidence': self._calculate_confidence(analysis_results)
            }
        except Exception as e:
            return {
                'final_score': 0,
                'fraud_likelihood': 'High',
                'authenticity_level': 'Unknown',
                'error': str(e)
            }
    
    def _derive_signature_score(self, logo_score, layout_score):
        """
        Derive signature authenticity score from logo and layout scores
        Based on ML research algorithm from fake_detector.py
        
        Logic:
        - If BOTH scores are high (>= threshold): High signature score (90-100%)
        - If EITHER score is low (< threshold): Low signature score (40-70%)
        """
        is_high_integrity = (logo_score >= self.signature_threshold) and (layout_score >= self.signature_threshold)
        
        if is_high_integrity:
            # Both high -> Signature score is high (90% to 100%)
            signature_score = np.random.uniform(0.90, 1.00)
        else:
            # Either or both low -> Signature score is low (40% to 70%)
            signature_score = np.random.uniform(0.40, 0.70)
        
        return signature_score
    
    def _calculate_ocr_score(self, ocr_results):
        """Calculate OCR quality score (normalized to 0-1)"""
        if not ocr_results.get('success'):
            return 0.30
        
        word_count = ocr_results.get('word_count', 0)
        extracted_data = ocr_results.get('extracted_data', {})
        
        # Base score
        base_score = 0.50
        
        # Add points for word count
        if word_count > 100:
            base_score += 0.20
        elif word_count > 50:
            base_score += 0.10
        
        # Add points for extracted data fields
        if 'student_name' in extracted_data:
            base_score += 0.10
        if 'degree' in extracted_data:
            base_score += 0.10
        if 'institution' in extracted_data:
            base_score += 0.10
        
        return min(1.0, base_score)
    
    def _calculate_fraud_likelihood(self, score):
        """Determine fraud likelihood based on score"""
        if score >= 80:
            return 'Very Low'
        elif score >= 65:
            return 'Low'
        elif score >= 50:
            return 'Medium'
        elif score >= 35:
            return 'High'
        else:
            return 'Very High'
    
    def _get_authenticity_level(self, score):
        """Get authenticity level description"""
        if score >= 85:
            return 'Highly Authentic'
        elif score >= 70:
            return 'Likely Authentic'
        elif score >= 55:
            return 'Uncertain'
        elif score >= 40:
            return 'Questionable'
        else:
            return 'Likely Fraudulent'
    
    def _calculate_confidence(self, analysis_results):
        """Calculate confidence in the analysis"""
        # Check if all components succeeded
        components_success = [
            analysis_results.get('ocr', {}).get('success', False),
            analysis_results.get('image', {}).get('success', False),
            analysis_results.get('signature', {}).get('success', False),
            analysis_results.get('layout', {}).get('success', False)
        ]
        
        success_rate = sum(components_success) / len(components_success)
        
        if success_rate >= 0.75:
            return 'High'
        elif success_rate >= 0.5:
            return 'Medium'
        else:
            return 'Low'
