import redis.asyncio as redis

# Create a global Redis client
redis_client = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)
log_key = "ai_analysis"


# Set a value asynchronously
async def set_redis_value(text: str) -> None:
    print(text)
    old = await get_redis_values()
    old = old if old == "" else f"{old}\n"
    await redis_client.set(log_key, f"{old}{text}", ex=3600)


# Get a redis value based on the key
async def get_redis_values() -> str:
    value = await redis_client.get(log_key)
    return value if value else ""


# Flush the current Redis DB
async def flush_redis_db() -> None:
    await redis_client.set(log_key, "", ex=3600)
    await redis_client.flushdb()
