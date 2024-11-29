from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import requests
from random import randint
import logging

logging.basicConfig(level=logging.INFO)

# Retry configuration
MAX_RETRIES = 5
RETRY_WAIT_SECONDS = 20

def should_fail():
    return randint(0, 1) == 0  # 50% chance of failure

# Retryable POST request
@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(RETRY_WAIT_SECONDS),
    retry=retry_if_exception_type(requests.RequestException),
)
def make_post_request(url, data, headers):
    # retry demo
    logging.info("Attempting POST request...")
    # if should_fail():
    #   raise requests.RequestException("Simulated failure for retry testing")
    logging.info("POST request succeeded!")
    return requests.post(url, data=data, headers=headers)

# Retryable GET request
@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_fixed(RETRY_WAIT_SECONDS),
    retry=retry_if_exception_type(requests.RequestException),
)
def make_get_request(url, headers, params):
    return requests.get(url, headers=headers, params=params)
