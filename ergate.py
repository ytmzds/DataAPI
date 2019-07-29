# developer : prince biscuit
# time : 2018/6/29
# version : 0.0.1
# simple spider tools

import requests
# 第三方库


import threading
import time
import json


# 标准库


def download_page(url, show_error=False, charset=None, **kwargs) -> str:
    '''下载页面，依赖requests'''

    try:
        res = requests.get(url, **kwargs)
        res.raise_for_status()
        if not charset:
            res.encoding = res.apparent_encoding
        else:
            res.encoding = charset
        return res.text
    except Exception as e:
        if show_error:
            print(e)
        return None


def download_file(url, filepath, show_error=False, **kwargs) -> bool:
    '''下载小型文件，依赖requests'''

    try:
        res = requests.get(url, **kwargs)
        res.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(res.content)
        return True
    except Exception as e:
        if show_error:
            print(e)
        return None


def is_url_valid(url, **kwargs) -> bool:
    try:
        res = requests.head(url, **kwargs)
        res.raise_for_status()
        return True
    except:
        return False


class Timer:
    '''计时器类
    该类的主要作用是配合下面的Worker类'''

    def __init__(self, interval=1):
        self.interval = interval
        self.timer = [time.time(), 0]

    def tick(self):
        '''当经历指定的秒数后返回真值,随后继续计时'''

        self.timer[1] = time.time()
        if self.timer[1] - self.timer[0] >= self.interval:
            self.timer[0] = self.timer[1]
            return True
        return False

    def set_interval(self, new_value):
        '''修改时间间隔'''

        self.interval = new_value


class ThreadPrototype(threading.Thread):
    '''由于Python的线程类并不是非常的一体化，所以还是需要自己构建非常多的东西
       这里是对线程做一个简单的封装，使得这个线程在主循环当中可以实现比较方便的暂停,恢复和终止'''

    def __init__(self):
        threading.Thread.__init__(self)
        self.wait = threading.Event()
        self.running = threading.Event()
        self.wait.set()
        self.running.set()

    def stop(self):
        '''停止线程'''

        self.wait.set()
        self.running.clear()

    def pause(self):
        '''暂停线程'''

        self.wait.clear()

    def resume(self):
        '''恢复线程'''

        self.wait.set()


class SingleWorker(ThreadPrototype):
    ''''''

    def __init__(self, threadfunc, args=None, callback=None):

        ThreadPrototype.__init__(self)
        self.thread_func = threadfunc
        self.args = args
        self.callback = callback

    def get_result(self):

        return self.result

    def run(self):

        while self.running.is_set():
            if self.wait.is_set():
                try:
                    self.result = self.thread_func(*self.args)
                    if self.result:
                        self.callback()
                except:
                    self.result = None
                self.stop()


class Worker(ThreadPrototype):
    '''该类是一个线程类,和大多数普通的线程一样执行一个函数作为自己的任务,该类本身没有太多的特色
    它主要是作为WorkerFactory类控制的行动单元,就像是工厂里的员工一样,WorkerFactory会根据事先设定
    的值来控制同一时间内一起运行的线程数量,在不超过这个数量的前提下进行大批量的工作分配...'''

    def __init__(self, threadfunc, args, groups, rest):

        ThreadPrototype.__init__(self)
        self.threadfunc = threadfunc
        self.args = args
        self.groups = groups
        self.rest = rest
        self.groups.append(self)

    def run(self):
        '''执行函数,在保证函数成功执行的前提下返回函数的结果,如果函数执行出现错误,该线程会终结,并且结果为None'''

        while self.running.is_set():
            if self.wait.is_set():
                try:
                    self.result = self.threadfunc(*self.args)
                except:
                    self.result = None
                self.groups.remove(self)
                self.rest.append(self)
                self.stop()

    def get_result(self):
        '''返回线程执行完毕后,获得函数返回的结果'''

        return self.result


class WorkerFactory:

    def __init__(self):

        self.workers = []
        self.rest = []
        # 该类主要控制两个列表,第一个列表保存着所有正在运行的线程,每当一个线程运行结束,就会把自己移动到rest列表中
        # 表示已经运行结束,每一个被运行结束的线程都会执行他们的回调函数,回调函数必须事先设定...回调函数一般用于显示进度并且
        # 获得每一个线程函数执行的结果

    def produce_limitation(self, argses, thread_func, callback, limitation=3):
        '''use limitation as the most number of the thread number at one time
        limitation代表了同一时间内最多可以有多少线程在运行着'''

        for args in argses:
            while (1):
                if len(self.workers) < limitation:
                    temp = Worker(thread_func, args, self.workers, self.rest)
                    temp.start()
                    temp.join()
                    break

            while len(self.rest) > 0:
                now = self.rest.pop()
                callback(now)

    def produce(self, argses, thread_func, callback):
        '''use thread_func with args save in objs
        produce函数和produce_limitation函数是一样的,只不过它不限制数量,
        所以produce_limitation是produce的特殊情况'''

        for args in argses:
            temp = Worker(thread_func, args, self.workers, self.rest)
            temp.start()
            temp.join()

            while len(self.rest) > 0:
                now = self.rest.pop()
                callback(now)


class ProgressBar:
    '''进度条类,显示任务进度'''

    def __init__(self, max_value):

        self.value = 0
        self.max_value = max_value

    def show(self):

        if self.value != self.max_value:
            now = int((self.value / self.max_value) * 50)
            remain = 50 - now
            print("[", "#" * now + " " * remain, "]", end="\r")
        else:
            print("[", "#" * 50, "]")
            print("------------------------------------")
            self.value = 0


class LogType:
    NORMAL = 0
    WARNING = 1
    ERROR = 2
    UNKNOW = 3

    @staticmethod
    def get_label(t_):

        if t_ == LogType.WARNING:
            return "[WARNING]"
        elif t_ == LogType.NORMAL:
            return "[NORMAL]"
        elif t_ == LogType.ERROR:
            return "[ERROR]"
        else:
            return "[UNKNOW]"


class Logger:

    def __init__(self, filename):
        self.info_list = []

    def log(self, message, t_: int, position="program"):
        log_tuple = (LogType.get_label(t_), self.temp_time(), position, message)
        log = "%s %s %s %s" % log_tuple
        self.info_list.append(log)

    def temp_time(self):
        t = time.localtime()
        time_tuple = (t[0], t[1], t[2], t[3], t[4], t[5])
        return "%d-%d-%d  %d:%d:%d" % time_tuple

    def pass_list(self):
        for msg in self.info_list:
            print(msg)

    def remark(self, info):
        self.info_list.append(info)


class JsonConfiger:
    '''读取来自于Json文件中的配置信息
    该类不提供一体化的功能,只作为函数集合体'''

    @staticmethod
    def read_all(filepath, encoding="utf-8") -> dict:
        '''读取所有的配置信息并返回'''

        try:
            with open(filepath, "r", encoding=encoding) as f:
                return json.load(f)
        except:
            return None

    @staticmethod
    def read_key(filepath, key, encoding="utf-8"):
        '''读取一个键值'''

        try:
            obj = JsonConfiger.read_all(filepath, encoding=encoding)
            return obj.get(key)
        except:
            return None

    @staticmethod
    def _read_keys(obj, keys):
        '''同read_keys但是没有读取文件的过程'''

        try:
            for key in keys:
                obj = obj[key]
            return obj
        except:
            return None

    @staticmethod
    def read_keys(filepath, keys: list, encoding="utf-8"):
        '''深度读取键值'''

        try:
            obj = JsonConfiger.read_all(filepath, encoding=encoding)
            return JsonConfiger._read_keys(obj, keys)
        except:
            return None

    @staticmethod
    def write_key(filepath, key, value, encoding="utf-8") -> bool:
        '''重写一个键值'''

        try:
            obj = JsonConfiger.read_all(filepath, encoding=encoding)
            obj[key] = value
            with open(filepath, "w", encoding=encoding) as f:
                json.dump(obj, f)
            return True
        except:
            return False

    @staticmethod
    def write_keys(filepath, keys, value, encoding="utf-8") -> bool:
        '''重写一个深度键值'''

        def __get_obj(obj, keys):

            for i in range(len(keys) - 1):
                obj = obj[keys[i]]
            return obj

        try:
            target = JsonConfiger.read_all(filepath, encoding=encoding)
            __get_obj(target, keys)[keys.pop()] = value
            with open(filepath, "w", encoding=encoding) as f:
                json.dump(target, f)
            return True
        except Exception as e:
            print(e)
            return False


class ElecBox(ThreadPrototype):
    '''this class contain a function
    and it will mark itself when the function is over'''

    @staticmethod
    def _switch_off(that_box, callback):

        def _new_callback():
            '''callback function must to stop father thread'''

            that_box.stop()
            if callback: callback()

        return _new_callback

    def __init__(self, action, callback=None, *args, **kwargs):
        super(ElecBox, self).__init__()

        self.__over = False
        self.__action = action
        self.__args = args
        self.__kwargs = kwargs
        self.__callback = ElecBox._switch_off(self, callback)
        self.result = None

    def rumble(self):
        '''run this function , and if function over
        the mark self.__over will be set True'''

        self.result = self.__action(*self._ElecBox__args, **self._ElecBox__kwargs)
        self._ElecBox__over = True
        self._ElecBox__callback()

    def is_over(self):

        return self._ElecBox__over

    def get_result(self):
        '''get action's result'''

        return self.result

    def run(self):

        while self._running.is_set():
            if self._wait.is_set():
                self.rumble()

    def __call__(self, joint=False):

        self.start()
        if joint: self.join()


def ElecBoxInstaller(callback, joint):
    def _(func):
        def _copy_box(*args, **kwargs):
            ElecBox(func, callback, *args, **kwargs)(joint)

        return _copy_box

    return _
