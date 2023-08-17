import openai


class OpenAIErrors:

    @staticmethod
    def is4xxErrors(http_status: str):
        if http_status.startswith("4"):
            return True
        return False

    @staticmethod
    def is5xxErrors(http_status: str):
        if http_status.startswith("5"):
            return True
        return False

