from typing import Any
from fastapi.responses import JSONResponse

def success_response(data: Any):
    return JSONResponse(
        content={
            "success": True,
            "successMessage": "Data retrieved successfully.",
            "data": data,
            "errorMessage": None,
            "statusCode": "200",
        },
        status_code=200,
    )

def error_response():
    return JSONResponse(
        content={
            "success": False,
            "successMessage": None,
            "data": None,
            "errorMessage": "Network Is Busy, Try After Sometime",
            "statusCode": "404",
        },
        status_code=404,
    )
