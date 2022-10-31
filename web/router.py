from fastapi.routing import APIRouter

from web.routers import book_types


api_router = APIRouter()

api_router.include_router(book_types.router, prefix="/book_types", tags=["Book Types"])