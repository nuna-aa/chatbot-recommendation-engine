from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.prompts import load_prompt
import os


class PromptService:
    def __init__(self):
        self.__file_name = 'configuration/prompt.yaml'

    def __load_system_prompt(self):
        root_directory = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_directory, self.__file_name)
        return load_prompt(config_path)

    def __set_system_template(self):
        system_prompt = self.__load_system_prompt().format()
        return SystemMessagePromptTemplate.from_template(system_prompt)

    def __set_human_template(self):
        human_template = "{question}"
        return HumanMessagePromptTemplate.from_template(human_template)

    def set_chat_message_prompt(self):
        chat_prompt = ChatPromptTemplate.from_messages([self.__set_system_template(), self.__set_human_template()])
        return chat_prompt
