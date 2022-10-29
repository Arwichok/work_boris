import secrets
import random
RANGE = 10**6


def get_pin() -> str:
    return str(random.randrange(RANGE))
