from fastapi import status


class ResponseException(Exception):

    def __init__(self, message: str, code: str):
        self.http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message
        self.code = code
