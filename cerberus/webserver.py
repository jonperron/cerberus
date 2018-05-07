#! /usr/bin/python3

import falcon
import logging
import redis

from datetime import datetime

def get_redis_client(
    host='localhost',
    port=6379,
    db=0,
    password=None,
    charset='utf-8',
    decode_responses=True
):
    redis_client = redis.StrictRedis(
        host=host,
        port=port,
        db=db,
        password=password,
        charset=charset,
        decode_responses=decode_responses,
    )
    return redis_client


class StorageEngine:
    """
    DB Engine compatible using Redis.
    """
    def __init__(self, *args, **kwargs):
        self.redis_client = get_redis_client()
		
    def get_last_detection(self):
        return datetime.strptime(self.redis_client.get('last_detection'), '%Y-%m-%dT%H:%M:%S.%f').replace(microsecond=0) if self.redis_client.get('last_detection') else None

    def save_last_detection(self):
        return self.redis_client.set('last_detection', datetime.now().isoformat())
		
    def get_detection_amount(self):
        return self.redis_client.get('detection_amount')
		
    def save_detection_amount(self, amount):
        """
        :param amount: Amount of detection
        :type amount: int.
        """
        return self.redis_client.set('detection_amount', amount)

    def get_cerberus_status(self):
        return self.redis_client.get('guard_status') if self.redis_client.get('guard_status') else 'Unknown'
        
    def save_cerberus_status(self, status):
        """
        Update states.
        :param status: Cerberus' status.
        :type status: str.
        """
        return self.redis_client.set('guard_status', status)

class StorageError(Exception):
    """
    Handle Storage Error (Redis unavailable etc)
    """
    @staticmethod
    def handle(ex, req, resp, params):
        description = 'A teapot is not a database you know ?'
        raise falcon.HTTPError(falcon.HTTP_418, 'Database error', description)


class BaseAPI:
    """
    Base API template.
    """
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('api')

    def redis_unavailable(self, exception):
        self.logger.error(exception)
        description = 'Sorry, not able to speak with my memory.'
        raise falcon.HTTPServiceUnavailable(
            'Service down',
            description, 
            30
        )


class LastDetection(BaseAPI):
    """
    Get last detection date or save new detection.
    """
    def on_get(self, req, resp):
        try:
            last_detection = db.get_last_detection()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"last_detection": last_detection.isoformat()}
        except Exception as e:
            self.redis_unavailable(e)

    def on_post(self, req, resp):
        try:
            last_detection = db.save_last_detection()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"last_detection": "updated"}
        except Exception as e:
            self.redis_unavailable(e)


class CountAmountofDetection(BaseAPI):
    """
    Get or save amount of detection.
    """
    def on_get(self, req, resp):
        try:
            detection_amount = int(self.db.get_detection_amount()) if self.db.get_detection_amount() else 0
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"detections": detection_amount}
        except Exception as e:
            self.redis_unavailable(e)
            
    def on_post(self, req, resp):
        try:
            previous_amount = int(self.db.get_detection_amount()) if self.db.get_detection_amount() else 0
            self.db.save_detection_amount(previous_amount + 1)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"detections" : "updated"}
        except Exception as e:
            self.redis_unavailable(e)


class CerberusStatus(BaseAPI):
    """
    Get or save Cerberus status.
    """
    def on_get(self, req, resp):
        try:
            status = self.db.get_cerberus_status()
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"status": status}
        except Exception as e:
            self.redis_unavailable(e)
            
    def on_post(self, req, resp):
        try:
            status = req.media.get('status', None)
            self.db.save_cerberus_status(status)
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.media = {"status": "updated"}     
        except Exception as e:
            self.redis_unavailable(e)

# Falcon App definition
app = falcon.API()
db = StorageEngine()
# Define API routes
app.add_route('/new_detection', LastDetection(db))
app.add_route('/detection_amount', CountAmountofDetection(db))
app.add_route('/cerberus_status', CerberusStatus(db))
