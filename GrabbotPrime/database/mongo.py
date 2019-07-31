from pymongo import MongoClient
import logging

log = logging.getLogger(__name__)

class MongoDatabase:

    class UpdateOperator:
        CURRENT_DATE = "$currentDate"
        INCREMENT = "$inc"
        MIN = "$min"
        MAX = "$max"
        MULTIPLY = "$mul"
        RENAME = "$rename"
        SET = "$set"
        SET_ON_INSERT = "$setOnInsert"
        UNSET = "$unset"

    DATABASE_NAME = "grabbot_prime"
    
    def __init__(self, address):
        self.address = address
        self._connect()

    def _connect(self):
        log.info(f"Connecting to MongoDB server at '{self.address}'...")
        
        self.client = MongoClient(self.address)
        self.db = self.client[MongoDatabase.DATABASE_NAME]
        
        log.info("Connected.")

    def insert(self, collection, data_filter, data, upsert=True, update_operator=UpdateOperator.SET):

        log.debug(f"Attempting {'upsert' if upsert else 'insert'}:")
        log.debug(f"    Operation: {update_operator}")
        log.debug(f"    Filter: {data_filter}")
        log.debug(f"    Data: {data}")
        
        result = self.db[collection].update_one(data_filter, { "$set": data }, upsert=upsert)

        log.debug(f"{result.modified_count} record(s) updated.")

    def get_all_records(self, collection):
        log.debug(f"Getting all records for collection '{collection}'...")
        return list(self.db[collection].find({}))
