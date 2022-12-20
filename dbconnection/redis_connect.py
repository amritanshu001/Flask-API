import redis

blocklist_connection = redis.Redis(
    host='redis-19042.c301.ap-south-1-1.ec2.cloud.redislabs.com',
    port=19042,
    password='5TXj5pax2zKfYtZQxOoFTu4uAMffO88B')
