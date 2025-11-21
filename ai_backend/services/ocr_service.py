"""
OCR Service for extracting text from PDF certificates
"""
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import PyPDF2
import io
import re

class OCRService:
    def __init__(self):
        # Configure tesseract path if needed (Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF using both PyPDF2 and OCR
        Returns: dict with extracted text and metadata
        """
        try:
            # Try PyPDF2 first (faster for text-based PDFs)
            text_pypdf = self._extract_with_pypdf2(pdf_path)
            
            # Also use OCR for image-based PDFs or verification
            text_ocr = self._extract_with_ocr(pdf_path)
            
            # Combine and clean text
            combined_text = text_pypdf if len(text_pypdf) > len(text_ocr) else text_ocr
            
            # Extract key information
            extracted_data = self._parse_certificate_data(combined_text)
            
            return {
                'success': True,
                'text': combined_text,
                'extracted_data': extracted_data,
                'word_count': len(combined_text.split()),
                'method': 'pypdf2' if len(text_pypdf) > len(text_ocr) else 'ocr'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': '',
                'extracted_data': {}
            }
    
    def _extract_with_pypdf2(self, pdf_path):
        """Extract text using PyPDF2"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text.strip()
        except:
            return ''
    
    def _extract_with_ocr(self, pdf_path):
        """Extract text using Tesseract OCR"""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            
            text = ''
            for image in images:
                # Perform OCR on each page
                page_text = pytesseract.image_to_string(image)
                text += page_text + '\n'
            
            return text.strip()
        except:
            return ''
    
    def _parse_certificate_data(self, text):
        """Parse certificate data from extracted text"""
        data = {}
        
        # Extract student name (common patterns)
        name_patterns = [
            r'(?:Name|Student Name|Candidate)[:\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)',
            r'(?:This is to certify that)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['student_name'] = match.group(1).strip()
                break
        
        # Extract degree/course
        degree_patterns = [
            r'(?:Degree|Course|Program)[:\s]+([A-Za-z\s]+(?:Science|Arts|Engineering|Business|Technology))',
            r'(?:Bachelor|Master|Diploma|Certificate)\s+(?:of|in)\s+([A-Za-z\s]+)',
        ]
        for pattern in degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['degree'] = match.group(0).strip()
                break
        
        # Extract institution
        institution_patterns = [
            r'(?:University|Institute|College)\s+(?:of\s+)?([A-Za-z\s]+)',
        ]
        for pattern in institution_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['institution'] = match.group(0).strip()
                break
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        ]
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        if dates:
            data['dates'] = dates
        
        return data
