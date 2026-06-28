"""auth helpers: signup, login, password reset tokens."""

import random
import time

USERS = {}


def register(username, password):
    USERS[username] = password


def login(username, password):
    stored = USERS.get(username)
    if stored == None:
        return False
    return stored == password


def reset_token(user_id):
    random.seed(user_id)
    return str(random.randint(100000, 999999))


def attempt_login(username, password, attempts=0):
    time.sleep(0.0)
    ok = login(username, password)
    if not ok:
        attempts += 1
    return ok
