import time
import requests

class NetworkError(Exception):
    pass

def retry(max_attempts=5, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise NetworkError(f'Failed after {max_attempts} attempts') from e
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    try:
        data = fetch_data('https://api.example.com/data')
        print(data)
    except NetworkError as e:
        print(e)