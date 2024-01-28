import redis
import os
from rq import Worker, Queue, Connection

redis_connection = redis.Redis(host=os.getenv('REDIS'), port=6379)
queue = Queue(connection=redis_connection)

with Connection(redis_connection):
    worker = Worker([queue], connection=redis_connection)
    worker.work()