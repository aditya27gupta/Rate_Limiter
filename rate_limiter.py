import datetime
from collections import defaultdict, deque

user_rates = defaultdict(deque)
request_limit = 5
time_limit = 60


def rate_limit(user_token: str) -> tuple[bool, int]:
    last_usages = user_rates[user_token]
    cur_datetime = datetime.datetime.now(tz=datetime.UTC)
    if len(last_usages) == request_limit:
        difference = cur_datetime - last_usages[0]
        last_request_seconds = difference.total_seconds()
        if last_request_seconds > time_limit:
            last_usages.popleft()
        else:
            return False, int(time_limit - last_request_seconds)
    last_usages.append(cur_datetime)
    return True, 0
