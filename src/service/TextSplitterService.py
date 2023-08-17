from langchain.text_splitter import RecursiveCharacterTextSplitter
from service.ConfigurationParser import ConfigurationParser as cp


class TextSplitterService:
    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__chunk_size = configurations["text"]["chunk"]["size"]
        self.__chunk_overlap = configurations["text"]["chunk"]["overlap"]
        self.__text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.__chunk_size,
            chunk_overlap=self.__chunk_overlap,
            length_function=len)

    def split(self, documents):
        return self.__text_splitter.split_documents(documents)
