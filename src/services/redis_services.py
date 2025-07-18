import redis as redis

# Create a global Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
log_key = "ai_analysis"


# Set a value hronously
def set_redis_value(text: str) -> None:
    print(text)
    old = get_redis_values()
    old = old if old == "" else f"{old}\n"
    redis_client.set(log_key, f"{old}{text}", ex=3600)


# Get a redis value based on the key
def get_redis_values() -> str:
    value = redis_client.get(log_key)
    return str(value) if value else ""


# Flush the current Redis DB
def flush_redis_db() -> None:
    redis_client.set(log_key, "", ex=3600)
    redis_client.flushdb()
