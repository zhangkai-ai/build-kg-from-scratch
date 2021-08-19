#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
联想服务化
"""

import json
import sys
import datetime
from loguru import logger
import tornado.web
from tornado.httpserver import HTTPServer
import main_handler

port = 19611


class BotHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        logger.info('post in', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        try:
            data = self.request.body
            logger.info(data)
            # 参数异常判断
            if data:
                dm_in_dict = json.loads(data)
                text = dm_in_dict['text']
                user_id = dm_in_dict['user_id']
                rst = main_handler.sent_handler(text, user_id)
                self.write({
                    "code": 0,
                    "message": "",
                    "data": rst,
                })
            else:
                self.write({
                    "code": 0,
                    "message": "para wrong",
                    "data": []
                })
        except Exception as e:
            self.write({
                "code": 0,
                "message": repr(e),
                "data": []
            })
        sys.stdout.flush()


application = tornado.web.Application([
    (r"/bot", BotHandler)
],
    autoreload=True
)


if __name__ == "__main__":
    server = HTTPServer(application)
    server.bind(port)
    logger.info("association bot demo is running!")
    server.start(num_processes=1)
    tornado.ioloop.IOLoop.current().start()
