from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.schemas.health import HealthOut

app = FastAPI(
    title='Finanças API',
    version=__version__,
    description='Este projeto é uma API RESTful self-hosted de '
    'código aberto para gerenciamento de finanças pessoais.',
)

app.add_middleware(
    CORSMiddleware,  # type: ignore[arg-type]
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health', response_model=HealthOut)
async def health():
    return {'status': 'ok'}
