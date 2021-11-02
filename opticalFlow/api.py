import logging

from fastapi import (
    FastAPI,
    # HTTPException,
    status,
    # Body,
    # Path,
    # File,
    # UploadFile,
    # Response
)

import farnebackOpticalFlow
import lucasKanadeOpticalFlow
from schemas import FarneBack, LucasKanade


logger = logging.getLogger('uvicorn.error')

app = FastAPI()

@app.get('/info/',
         tags=['Service'])
def info():
    return {"message": "This is api of Waldo optical flow CV"}

@app.get('/health/',
         tags=['Service'])
def health():
    return {"status": "UP"}

"""Methods for CV might use in future FileResponse object in case of returning video as well"""

@app.post('/farne_back_optical_flow/',
          tags=['CV Methods'],
          status_code=status.HTTP_200_OK)
def farne_back_optical_flow(*, 
                            # video_clip: UploadFile = File(...), # For later use for uploading video clip file
                            request: FarneBack = None):
    """Method for executing Farne Back Algorithm
       Later will be added additional needed params and also a proper file upload
    """
    logger.info(
        {
            "message": "Got Success Request on Farne Back method",
            # "video_clip_name": video_clip.__dict__['filename'],
            "request": request
        }
    )
    # Configuration as dict from request and SpooledTemporaryFile as video_clip can be provided
    farne_result = farnebackOpticalFlow.farne_back_optical_flow() # for now cv methods return None
    # Additional result params can be added later for returning via api call
    return {"status": "success",
            "message": "Farne Back optical flow executed successfully"}

@app.post('/lucas_kanade_optical_flow/',
          tags=['CV Methods'],
          status_code=status.HTTP_200_OK)
def lucas_kanade_optical_flow(*, 
                            #   video_clip: UploadFile = File(...), # For later use for uploading video clip file
                              request: LucasKanade = None):
    """Method for executing Lucas Kanade Algorithm
       Later will be added additional needed params and also a proper file upload
    """
    logger.info(
        {
            "message": "Got Success Request on Lucas Kanade method",
            # "video_clip_name": video_clip.filename,
            "request": request
        }
    )
    # Configuration as dict from request and SpooledTemporaryFile as video_clip can be provided
    lucas_result = lucasKanadeOpticalFlow.lucas_kanade_optical_flow() # for now cv methods return None
    # Additional result params can be added later for returning via api call
    return {"status": "success",
            "message": "Lucas Optical flow executed successfully"}
