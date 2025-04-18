import requests
import concurrent.futures


def task_process(url):
    headers = {"Content-Type": "application/json"}
    body = {"name": "zk"}
    response = requests.post(
        url,
        headers=headers,
        json=body
    )
    print(response.json(), flush=True)


def async_test():
    url = "http://127.0.0.1:8000/api/get-user"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for _ in range(10)]
    concurrent.futures.wait(futures)


if __name__ == '__main__':
    async_test()

    print("done")
