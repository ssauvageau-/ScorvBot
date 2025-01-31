from enum import Enum


class RedisKeys(Enum):
    TAGS = "tags"
    RAFFLE_CFG = "raffle_config"
    RAFFLE_SUB = "raffle_submissions"
    DELAY = "foa_delay"
    GUILD_CONFIG = "guild_config"
