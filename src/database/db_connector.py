from src.logger import logging
from src.exception import CustomException
from datetime import datetime
from src.constant import DATA_BASE_NAME,MONGODB_URL_GITFIT

from src.constant import *

import os,sys
import pymongo
import certifi

ca = certifi.where()

class MongoDBClient:
    """
    Class Name :   export_data_into_feature_store
    Description :   This method exports the dataframe from mongodb feature store as dataframe 
    
    Output      :   connection to mongodb database
    On Failure  :   raises an exception
    """
    client = None

    def __init__(self, database_name=DATA_BASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_GITFIT)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_GITFIT} is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection succesfull")
        except Exception as e:
            raise CustomException(e,sys)