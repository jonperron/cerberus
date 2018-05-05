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
        return self.redis_client.get('detection_amount', amount)


class StorageError(Exception):
    """
    Handle Storage Error (Redis unavailable etc)
    """
    @staticmethod
    def handle(ex, req, resp, params):
        description = 'A teapot is not a database you know ?'
        raise falcon.HTTPError(falcon.HTTP_418, 'Database error', description)


class LastDetection:
    """
    Get last detection date or save new detection.
    """
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('lastdetection')

    def redis_unavailable(self, exception):
        self.logger.error(exception)
        description = 'Sorry, not able to speak with my memory.'
        raise falcon.HTTPServiceUnavailable(
            'Service down',
            description, 
            30
        )

    def on_get(self, req, resp):
        try:
            last_detection = db.get_last_detection()
            resp.status = falcon.HTTP_200
        except Exception as e:
            self.redis_unavailable(e)

    def on_post(self, req, resp):
        try:
            last_detection = db.save_last_detection()
            resp.status = falcon.HTTP_200
        except Exception as e:
            self.redis_unavailable(e)


class CountAmountofDetection(LastDetection):
    """
    Get or save amount of detection.
    """
    def on_get(self, req, resp):
        try:
            self.detection_amount = int(self.db.get_detection_amount()) if self.db.get_detection_amount() else 0
            resp.context['detection_amount'] = 0
            resp.status = falcon.HTTP_200
        except Exception as e:
            self.redis_unavailable(e)
            
    def on_post(self, req, resp):
        try:
            self.previous_amount = int(self.db.get_detection_amount()) if self.db.get_detection_amount() else 0
            self.db.save_detection_amount(self.previous_amount + 1)
            resp.status = falcon.HTTP_200
        except Exception as e:
            self.redis_unavailable(e)


# Falcon App definition
app = falcon.API()
db = StorageEngine()
# Define API routes
app.add_route('/new_detection', LastDetection(db))
app.add_route('/detection_amount', CountAmountofDetection(db))
