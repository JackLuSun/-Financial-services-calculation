# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:05:22 2019

@author: jackl
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:50:01 2019

@author: jackl
GOAL: 开发一个简陋的python在线运行网站，借助 python 框架flask 快速实现后端的简要开发
"""
from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/',methods=['GET'])# tell flask realation between URL and function who deals with the URL
def hello_world():
    r=""
    with open('index.html',encoding="utf8") as f:
        r = f.read() 
    return r


@app.route('/post_test',methods=['POST','GET'])# 前端向后端发送要执行的源代码时，URL为 post_test 对应着前端 post 时候指定的 url
def get_tasks():
    if request.method == 'POST':
        code = request.get_json(force=True)['code']# 前端那边采用json 格式,前端穿过来的数据指定放在了 'code' 关键字对应的值里
        # 将前端传来的python 程序保存并执行
        with open('code.py','w',encoding='utf8') as f:
            f.write(code)
        proc = subprocess.Popen(['python', 'code.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        consoleOutput = proc.communicate()[0]

        return consoleOutput
        
    return hello_world()
 
if __name__ == '__main__':
    app.run(host='111.186.1.46',port='2333')
    