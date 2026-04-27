from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import json

from services.hash_service import generate_phash_from_image
from services.gemini_service import analyze_media_authenticity
from firebase_setup import get_db

router = APIRouter()

@router.post("/api/upload")
async def upload_media(file: UploadFile = File(...), metadata: str = Form(...)):
    try:
        file_bytes = await file.read()
        meta = json.loads(metadata)
        
        # 1. Generate Perceptual Hash
        phash = generate_phash_from_image(file_bytes)
        
        if not phash:
            return JSONResponse(status_code=400, content={"error": "Could not extract pHash from media."})
            
        # 2. Analyze with Gemini
        analysis = analyze_media_authenticity(phash, file.filename)
        
        try:
           analysis_dict = json.loads(analysis)
        except:
           analysis_dict = {"raw_analysis": analysis}

        # 3. Store record in Firestore
        db = get_db()
        doc_ref = None
        if db:
            doc_ref = db.collection('media_fingerprints').document()
            doc_ref.set({
                'filename': file.filename,
                'phash': phash,
                'metadata': meta,
                'analysis': analysis_dict,
                'source': 'OfficialBroadcaster'
            })
            
        return JSONResponse(status_code=200, content={
            "message": "Media processed and protected",
            "phash": phash,
            "analysis": analysis_dict,
            "firestore_id": doc_ref.id if doc_ref else "DB_NOT_CONFIGURED"
        })
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
