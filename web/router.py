from fastapi.routing import APIRouter

from web.routers import (
    books,
    book_types,
    book_genres,
    publishers,
    departments,
    book_decommisions,
    students,
    book_states
)


api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["Books"])
api_router.include_router(book_types.router, prefix="/book_types", tags=["Book Types"])
api_router.include_router(book_genres.router, prefix="/book_genres", tags=["Book Genres"])
api_router.include_router(publishers.router, prefix="/publishers", tags=["Publishers"])
api_router.include_router(departments.router, prefix="/departments", tags=["Departments"])
api_router.include_router(book_decommisions.router, prefix="/book_decommisions", tags=["Book Decommisions"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])
api_router.include_router(book_states.router, prefix="/book_states", tags=["Book States"])