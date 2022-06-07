from fastapi import HTTPException, Request
from starlette.responses import JSONResponse


async def http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "message": str(exception.detail),
            "code": exception.status_code,
        },
    )
