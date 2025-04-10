import time


numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


class PlayMode:
    SINGLE_PLAYER = 1
    MULTI_PLAYER = 2
    NO_PLAYER = 3


class SideTable:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


player_symbol = {
    1: "🔵",
    2: "🔴",
}


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper