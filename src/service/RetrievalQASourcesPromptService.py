from langchain.prompts import load_prompt
import os


class RetrievalQASourcesPromptService:
    def __init__(self):
        self.__file_name = 'configuration/retrieval_qa_sources_prompt.yaml'

    def __load_system_prompt(self):
        root_directory = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_directory, self.__file_name)
        return load_prompt(config_path)

    def set_chat_message_prompt(self):
        return self.__load_system_prompt()
