import concurrent.futures
import requests


def task_process(url):
    response = requests.get(url)
    print(response.json(), flush=True)


def sycn_test():
    """
    同步阻塞
    server 5个进程并行处理
    client端10个并发请求
    整体阻塞时间，比100s少很多
    """
    url = "http://127.0.0.1:8000/sync-time-sleep/"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for _ in range(10)]
    concurrent.futures.wait(futures)


def async_test():
    """
    异步阻塞
    server 5个进程并行处理
    client端10个并发请求
    整体阻塞时间不变，还是10s
    (即如果代码是纯异步逻辑，则多进程是非性能必要的)
    """
    url = "http://127.0.0.1:8000/async-time-sleep/"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for i in range(10)]
    concurrent.futures.wait(futures)


if __name__ == '__main__':
    # sycn_test()

    async_test()

    print('done')
