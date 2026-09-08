from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self,error_code: str,status_code: int,message: str):
        self.error_code = error_code
        self.status_code = status_code
        self.message = message

async def app_exception_handler(request: Request,exc: AppException) -> JSONResponse:

    return JSONResponse(status_code=exc.status_code,
                        content={"error_code": exc.error_code,
                        "message": exc.message})        

class NotFoundException(AppException):
    def __init__(self, message:str, error_code: str = "NOT FOUND"):
        super().__init__(error_code=error_code, status_code=404, message=message)

class BadRequestException(AppException):
    def __init__(self, message: str, error_code: str = "BAD REQUEST"):
        super().__init__(error_code=error_code, status_code=400, message=message)

class UnauthorizedException(AppException):
    def __init__(self, message: str, error_code: str = "UNAUTHORIZED"):
        super().__init__(error_code=error_code, status_code=401, message=message)


# from fastapi import Request
# from fastapi.responses import JSONResponse

# class AppException(Exception):
#     """Base class for all application-specific exceptions."""
#     def __init__(self, error_code: str, status_code: int, message: str):
#         self.error_code = error_code
#         self.status_code = status_code
#         self.message = message

# async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
#     """Global handler for AppException. Returns a standardized JSON response."""
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "error": exc.error_code,
#             "message": exc.message,
#         }
#     )
