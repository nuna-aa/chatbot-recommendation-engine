class LLMResponseException(Exception):

    def __init__(self, http_status: str, message: str, code: str):
        self.http_status = http_status
        self.message = message
        self.code = code
