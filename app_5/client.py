import concurrent.futures
import requests


def task_process(url):
    response = requests.get(url)
    print(response.json(), flush=True)


def sync_test():
    url = "http://127.0.0.1:8000/api/sync-time-sleep"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for _ in range(10)]
    concurrent.futures.wait(futures)


if __name__ == '__main__':
    sync_test()

    print('done')