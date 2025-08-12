from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.service import Service
from models.models import ConversionRequest

router = APIRouter()

@router.post('/convert')
def convert(req: ConversionRequest):
    try:
        service = Service(req.user_query)
        response = service.model_interaction()
        return JSONResponse(content={'output_text': response})
    except Exception as e:
        print(f'Exception: {e}')
        return JSONResponse(content={'error': str(e)})
