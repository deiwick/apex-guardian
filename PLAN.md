# ApexGuardian File Structure Plan

This document outlines the file structure for the ApexGuardian project to ensure clear separation of concerns between our frontend client and Python FastAPI backend.

## Root Directory (`d:\projects\gdg\ApexGuardian`)

```text
ApexGuardian/
├── PLAN.md                  # This file
├── frontend/                # React UI, Tailwind CSS, Firebase config
└── backend/                 # FastAPI REST server, pHash, Gemini logic
```

### Frontend (`/frontend`)
Contains the user-facing web application.
- `index.html`: Entry point for Vite.
- `src/`
  - `App.jsx`: Main container component.
  - `main.jsx`: React entry point.
  - `index.css`: Global styles and Tailwind directives.
  - `firebaseSetup.js`: Config map and initialization for Firestore and Firebase Storage.
  - `components/`
    - `OfficialUpload.jsx`: The upload component where officially recognized media is uploaded by authorities.

### Backend (`/backend`)
Contains the logic for analyzing and persisting verification data.
- `requirements.txt`: Python package dependencies.
- `main.py`: The FastAPI application server and endpoints.
- `firebase_setup.py`: Logic initializing `firebase-admin` with a service account.
- `services/`
  - `hash_service.py`: Generates the pHash (Perceptual Hash) from the uploaded media.
  - `gemini_service.py`: Contextually processes metadata/content via Google Gemini API.
- `routers/`
  - `upload.py`: API endpoints for handling upload routes locally and proxying.
- `models/`
  - `media.py`: Pydantic models for request/response payloads.
