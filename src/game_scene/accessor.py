import redis
import pickle
from game_core import GameMatch


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)


def read_session(key: str) -> GameMatch | None:
    raw = redis.get(key)
    return pickle.loads(raw) if raw else None


def write_session(key: str, val: GameMatch) -> None:
    redis.set(key, pickle.dumps(val))


def end_session(key) -> None:
    redis.delete(key)
