import tornado.ioloop
import tornado.web
import tornado.websocket
from ShapeDetector import detect
import time
import traceback

class ConnectHandler(tornado.websocket.WebSocketHandler) :
    def check_origin(self, origin) :
        '''重写同源检查 解决跨域问题'''
        return True

    def open(self) :
        '''新的websocket连接后被调动'''
        self.write_message('Welcome')

    def on_close(self) :
        '''websocket连接关闭后被调用'''

    def on_message(self, message) :
        '''接收到客户端消息时被调用'''
        try:
            # print(len(message))
            start=time.time()
            result = detect(message)
            # print("time:"+str(time.time()-start))
            self.write_message(result)  # 向客服端发送
        except Exception as e:
            traceback.print_exc()

if __name__ == "__main__" :
    app = tornado.web.Application([ (r'/socket', ConnectHandler) ])
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
