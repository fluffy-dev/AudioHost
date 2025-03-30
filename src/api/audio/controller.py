from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
import os

from src.apps.audio.depends.service import IAudioService
from src.apps.audio.dto import UploadFileDTO

from src.api.protection import AuthUser

router = APIRouter(prefix="/audio", tags=["audio"])

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",       # MP3
    "audio/wav",        # WAV
    "audio/ogg",        # OGG
    "audio/x-wav",      # WAV alternative
    "audio/x-m4a",      # M4A
    "audio/mp4",        # MP4 audio
    "audio/aac",        # AAC
}

@router.get("/")
async def list_files(user: AuthUser, service: IAudioService):
    try:
        return await service.list_audio_files(user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/file")
async def upload_file(file: UploadFile, file_description: str, user: AuthUser, service: IAudioService):
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    dto = UploadFileDTO(file_description=file_description,
                        user_id=user.id)

    try:
        return await service.upload_file(file, dto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file/{pk}")
async def stream_file(pk:int, user:AuthUser, service: IAudioService):

    try:
        file = await service.get_data(pk, user.id)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not os.path.exists(file.file_path):
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(file.file_path, "rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="application/octet-stream")

