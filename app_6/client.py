import requests
import concurrent.futures


def task_process(url):
    response = requests.get(url)
    print(response.json(), flush=True)


def sync_test():
    """
    同步阻塞，client端10个并发请求
    使用线程池进行异步封装
    整体阻塞时间：10s
    """
    # url = "http://127.0.0.1:8000/run-task/"
    # url = "http://127.0.0.1:8000/run-task-self-pool-1/"
    url = "http://127.0.0.1:8000/run-task-self-pool-2/"

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for _ in range(10)]
    concurrent.futures.wait(futures)


if __name__ == '__main__':
    sync_test()

    print("done")
