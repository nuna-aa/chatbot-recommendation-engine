from langchain.document_loaders import S3FileLoader
from service.ConfigurationParser import ConfigurationParser as cp


class S3FileTextLoaderService:
    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__bucket_name = configurations["s3"]["bucket"]

    def load_one(self, file_name):
        return S3FileLoader(self.__bucket_name, file_name).load()
