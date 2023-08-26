from langchain.document_loaders import S3DirectoryLoader
from service.ConfigurationParser import ConfigurationParser as cp


class S3DirectoryTextLoaderService:
    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__bucket_name = configurations["s3"]["bucket"]

        self.__loader = S3DirectoryLoader(self.__bucket_name)

    def load(self):
        return self.__loader.load()
