import redis, json, os
from typing import Literal

class EventHandler:
    conntext:redis.Redis
    type:Literal["send", "recv"]
    def __init__(self,_type:Literal["send", "recv"]):
        self.conntext = redis.Redis(host=os.environ["redis_host"], port=6379, db=0)
        self.type = _type
        if _type == "recv":
            self.conn = self.conntext.pubsub()
            self.conn.subscribe("event-handler")
        
    def itterate_events(self):
        return self.conn.listen()
    
    def raise_event(self, event:dict):
        if self.type == "send":
            self.conntext.publish("event-handler", json.dumps(event))
    
    def close(self):
        if self.conn:
            self.conn.close()
        self.conntext.close()

class Levels:
    ERROR = 0
    WARNING = 1
    INFO = 2
    STATUS = 3
    DEBUG = 4

class Events:
    ESTOP = {"level":Levels.ERROR,"msg":"Estop has been triggered"}
    INIT_DONE = {"level":Levels.STATUS, "msg":"cnc initalised", "status":"init"}
    ### expand as needed

    @staticmethod
    def get_custom(level:Literal["ERROR","WARNING","INFO","STATUS","DEBUG"], msg, **kwargs):
        return {"level":Levels.__dict__[level], "msg": msg, **kwargs}
