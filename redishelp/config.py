# run in commnad line 'redis-cli config set notify-keyspace-events KEA'
import redis
from wallet.helpers import send_money_back_to_sender_account
try:
    Redis = redis.Redis(host='0.0.0.0', port='6379', password='')
except:
    Redis = []

expired_time = 20


def check_redis_connection():
    try:
        Redis.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def check_in_cache(key):
    key = str(key)+":transactionhistory"
    return Redis.exists(key)


def delete_from_cache(key):
    key = str(key)+":transactionhistory"
    return Redis.delete(key)


def update_the_cache(key, value):
    key = str(key)+":transactionhistory"
    print key
    return Redis.set(key, value, expired_time)


def expiredkeysloop():
    import redis
    r = redis.StrictRedis(host='0.0.0.0', port='6379', password='')
    pubsub = r.pubsub()
    pubsub.psubscribe("*:transactionhistory")
    for msg in pubsub.listen():
        print msg
        try:
            if msg['type'] == "pmessage" and msg['data'] == "expired":
                id = msg['channel'].split(":")[1]
                send_money_back_to_sender_account(int(id))
                print msg
        except Exception,e:
            print str(e)
