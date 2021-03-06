from redistimeseries.client import Client
import redis
from collections import defaultdict
# from utils import QueueHashmap
import json

class RedisClient:
    """Constants"""
    TS_STORE_KEY = "nethive"
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if RedisClient.__instance == None:
            RedisClient()
        return RedisClient.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if RedisClient.__instance != None:
            # print("RedisClient is a singleton!")
            pass
        else:
            self.__ts_client = Client() # timeseries redis client
            self.__redis_client = redis.Redis() # general redis client
            # try:
            #     self.__ts_client.create(self.TS_STORE_KEY)
            # except Exception as e:
            #     pass
            RedisClient.__instance = self

    # Timeseries Query

    def ts_insert_http_bundle(self, store_key, package_id, timestamp, value, label):
        self.__ts_client.create(store_key, labels={'type': 'http'})
        return self.__ts_client.add(package_id, timestamp, value, labels=label)

    def ts_get_http_bundles(self, start_time, end_time):
        return self.__ts_client.mrange(start_time, end_time, filters=['type=http'], with_labels=True)
        # return self.__ts_client.info(key)
        # return self.__ts_client.mrange(start_time, end_time)
        # id = self.__ts_client.range(key, start_time, end_time)
    
    def ts_expire_http_bundle(self, package_id):
        self.__ts_client.alter(package_id, labels={"type":"expired"})
        key = "{}:{}".format(self.TS_STORE_KEY, package_id)
        return self.__ts_client.delete(key)

    # End of Timeseries Query    

    # Redis Query

    def store_http_request(self, key, value):
        return self.__redis_client.hmset(key, value)
    def get_http_request(self, key):
        # from_redis = self.__redis_client.hgetall(key)
        # self.__redis_client.delete(key)
        return self.__redis_client.hgetall(key)

    # End of Redis Query

    
