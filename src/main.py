"""
Entry point for the application.
Contains the following controller routes
/heath - Health check
/chat - Generate LLM response for user's message
/chat/data/reload - Reload all embeddings in the vector database
/chat/data/insert - Insert a single document in the vector database
"""

from typing import Any

from fastapi import FastAPI, Header, HTTPException, status, Depends, Request

import asyncio
from dto.UserMessage import UserMessage as um
from dto.HealthStatus import HealthStatus as hs
from dto.UserMessageRequest import UserMessageRequest as umr
from dto.SaveFileEmbedding import SaveFileEmbedding as sfe
from service.ChatService import ChatService as orch
from exception.LLMResponseException import LLMResponseException
from exception.ResponseException import ResponseException
from fastapi.responses import JSONResponse
import logging
import openai
import uvicorn
import sys

app = FastAPI()
reply = orch()

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")

"""
LLM response exception handler
"""
@app.exception_handler(LLMResponseException)
async def openai_client_exception_handler(request: Request, exc: LLMResponseException):
    logging.error("An error occurred", exc_info=True)
    return JSONResponse(
        status_code=int(exc.http_status),
        content={"message": f"{exc.message}", "code": f"{exc.code}"},
    )

"""
Response Exception Handler
"""
@app.exception_handler(ResponseException)
async def openai_client_exception_handler(request: Request, exc: ResponseException):
    logging.error("An error occurred", exc_info=True)
    return JSONResponse(
        status_code=exc.http_status,
        content={"message": f"{exc.message}", "code": f"{exc.code}"},
    )


"""
Request format validator
"""
def application_json(content_type: str = Header(...)):
    """Require request MIME-type to be application/json"""

    if content_type != "application/json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/json",
        )

"""
Health check endpoint
"""
@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=hs)
def getHealth() -> hs:
    return hs(status="OK")

"""
Chat endpoint to generate LLM response based on a user message
"""
@app.post("/chat", dependencies=[Depends(application_json)], response_model=um)
async def recommend(message: umr) -> Any:
    try:
        logging.info("Request: {%s}", message)
        llm_response = reply.recommend(message.message)
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)
    logging.info("Response: {%s}", llm_response)
    return llm_response

"""
Endpoint to refresh vector embeddings in the database
"""
@app.put("/chat/data/reload", dependencies=[Depends(application_json)])
async def reload_embeddings() -> Any:
    asyncio.create_task(process_reload())
    return  status.HTTP_202_ACCEPTED

"""
Endpoint to insert a single document in the vector database
"""
@app.post("/chat/data/insert", dependencies=[Depends(application_json)])
def save_file_embedding(fileName: sfe) -> Any:
    asyncio.create_task(save_one_file(fileName))
    return status.HTTP_202_ACCEPTED


async def save_one_file(fileName):
    try:
        collection_id = reply.insert_one_datasource(fileName.fileName)
        logging.info("File %s successfully saved in collection %s", fileName.fileName, collection_id)
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)


async def process_reload():
    try:
        collection_id = reply.reload_datasources()
        logging.info("reload successful for collection %s", collection_id)
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", timeout_keep_alive=5, reload=True)
