from typing import Any

from fastapi import FastAPI, Header, HTTPException, status, Depends, Request

from dto.UserMessage import UserMessage as um
from dto.ChatHistory import ChatHistory as ch
from dto.UserMessageRequest import UserMessageRequest as umr
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


@app.exception_handler(LLMResponseException)
async def openai_client_exception_handler(request: Request, exc: LLMResponseException):
    logging.error("An error occurred", exc_info=True)
    return JSONResponse(
        status_code=int(exc.http_status),
        content={"message": f"{exc.message}", "code": f"{exc.code}"},
    )


@app.exception_handler(ResponseException)
async def openai_client_exception_handler(request: Request, exc: ResponseException):
    logging.error("An error occurred", exc_info=True)
    return JSONResponse(
        status_code=exc.http_status,
        content={"message": f"{exc.message}", "code": f"{exc.code}"},
    )


def application_json(content_type: str = Header(...)):
    """Require request MIME-type to be application/json"""

    if content_type != "application/json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/json",
        )


@app.post("/chat", dependencies=[Depends(application_json)], response_model=um)
def recommend(message: umr) -> Any:
    try:
        llm_response = reply.recommend(message.message)
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)
    return llm_response


@app.get("/chat/history", dependencies=[Depends(application_json)], response_model=ch)
def recommend() -> Any:
    try:
        history = reply.get_chat_history()
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)
    return history


@app.delete("/chat/history/clear", dependencies=[Depends(application_json)], response_model=ch)
def recommend() -> Any:
    try:
        reply.clear_chat_history()
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)


@app.put("/chat/data/reload", dependencies=[Depends(application_json)])
def recommend() -> Any:
    try:
        reply.reload_datasources()
    except openai.error.OpenAIError as e:
        raise LLMResponseException(e.http_status, e.user_message, e.code)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise ResponseException(exc_value, exc_type)
    return status.HTTP_201_CREATED

def run():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", timeout_keep_alive=5)
