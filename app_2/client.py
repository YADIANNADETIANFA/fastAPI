import concurrent.futures
import requests


def task_process(url):
    response = requests.get(url)
    print(response.json(), flush=True)


def sycn_test():
    """
    对于同步阻塞，10个线程，10个请求，发现是串行处理
    整体阻塞时间：10 * 10 = 100s

    这也证明了：FastAPI确实是单进程、单线程，异步IO协程处理的。
    """
    url = "http://127.0.0.1:8000/sync-time-sleep/"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for i in range(10)]
    concurrent.futures.wait(futures)


def async_test():
    """
    对于异步阻塞，10个线程，10个请求，阻塞时间是重叠的
    整体阻塞时间：10s

    协程生效的原因：
        每个HTTP请求进来时，FastAPI + Uvicorn 会调用协程函数，生成协程对象，封装成task，注册到asyncio的event loop
        即，每一个HTTP请求都是一个独立的协程任务
        并且，所有的HTTP请求，**几乎都是同时进入。即所有的HTTP请求task，是几乎同时，在最开始就注册到event_loop中了。**
        不会在`await asyncio.sleep(10)`时，没有task任务可执行
    :return:
    """
    url = "http://127.0.0.1:8000/async-time-sleep/"
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(task_process, url) for i in range(10)]
    concurrent.futures.wait(futures)


if __name__ == '__main__':
    # sycn_test()

    async_test()

    print('done')
