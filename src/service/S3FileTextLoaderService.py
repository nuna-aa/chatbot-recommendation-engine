from langchain.document_loaders import S3FileLoader
from service.ConfigurationParser import ConfigurationParser as cp

"""
S3 File loader service. Loads a single file from the S3 bucket
"""
class S3FileTextLoaderService:
    def __init__(self):
        configurations = cp().get_configuration_properties()
        self.__bucket_name = configurations["s3"]["bucket"]

    """
    Load one file from S3 based on file name
    """
    def load_one(self, file_name):
        return S3FileLoader(self.__bucket_name, file_name).load()
