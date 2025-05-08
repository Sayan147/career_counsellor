import tempfile
import os
from fastapi import HTTPException
from contextlib import contextmanager
from pathlib import Path
import google.generativeai as genai
import pdf2image
import io
from PIL import Image
from ..core.config import get_settings
from ..db.mongodb import resumes_collection
from datetime import datetime

settings = get_settings()
genai.configure(api_key=settings.GOOGLE_API_KEY)

@contextmanager
def create_temp_file(contents, suffix='.pdf'):
    """Safely create and manage a temporary file."""
    temp_file = None
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        temp_file.write(contents)
        temp_file.flush()
        temp_file.close()
        yield temp_file.name
    finally:
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass

def convert_pdf_to_images(pdf_contents):
    """Convert all PDF pages to PNG images."""
    try:
        with create_temp_file(pdf_contents) as temp_pdf_path:
            # Convert all PDF pages to images
            images = pdf2image.convert_from_path(temp_pdf_path)
            
            if not images:
                raise ValueError("No images extracted from PDF")
            
            # Convert all pages to PNG bytes
            image_bytes_list = []
            for page in images:
                img_byte_arr = io.BytesIO()
                page.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                image_bytes_list.append(img_byte_arr.getvalue())
            
            return image_bytes_list
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting PDF to PNG: {str(e)}")

def extract_text_from_images(image_contents_list):
    """Extract text from multiple images using Gemini Vision."""
    try:
        # Initialize Gemini model for vision tasks
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        all_text = []
        for image_contents in image_contents_list:
            # Convert image bytes to base64
            image_parts = [
                {
                    "mime_type": "image/png",
                    "data": image_contents
                }
            ]
            
            # Generate prompt for vision model
            prompt = """Extract and analyze this resume. Focus on:
            1. Personal Information
            2. Education
            3. Work Experience
            4. Skills
            5. Projects
            6. Certifications
            
            Provide suggestions for improvement in each section."""
            
            # Get response from Gemini Vision
            response = model.generate_content([prompt, image_parts[0]])
            all_text.append(response.text)
        
        # Combine text from all pages
        combined_text = "\n\nPAGE BREAK\n\n".join(all_text)
        return combined_text
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from images: {str(e)}")

async def process_resume(user_id: str, pdf_contents: bytes):
    """Process resume and store results."""
    try:
        # Convert PDF to images
        image_contents_list = convert_pdf_to_images(pdf_contents)
        
        # Extract and analyze text
        analysis = extract_text_from_images(image_contents_list)
        
        # Store results in database
        await resumes_collection().insert_one({
            "user_id": user_id,
            "analysis": analysis,
            "timestamp": datetime.utcnow()
        })
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

async def get_resume_history(user_id: str) -> list:
    """Get user's resume analysis history."""
    cursor = resumes_collection().find(
        {"user_id": user_id},
        {"_id": 0}
    ).sort("timestamp", -1)
    return await cursor.to_list(length=None) 