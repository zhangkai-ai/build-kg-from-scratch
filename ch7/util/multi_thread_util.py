#!/usr/bin/env python
# -*- coding:utf8 -*-
from concurrent.futures import *
from loguru import logger


class ThreadFactory:

    def __init__(self):
        self.max_executor = 20
        self.running = 0
        self.executor = ThreadPoolExecutor(max_workers=self.max_executor)

    def add_thread(self, func, *args, **kw):
        fu = self.executor.submit(func, *args, **kw)
        return fu

    def get_rst(self, executor, timeout=100):
        try:
            rst = executor.result(timeout=timeout)
            return rst
        except Exception as e:
            logger.error(e)
            return None


thread_factory = ThreadFactory()
