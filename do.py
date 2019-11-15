# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:50:01 2019

@author: jackl
GOAL: 开发一个简陋的python在线运行网站，借助 python 后端框架flask 快速实现后端的简要开发
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

# 这里只是为了回复前端 GET 请求 js 文件，这里手法拙劣，flask 中应该有更好的方法
@app.route('/Webgraphviz_files/viz.js',methods=['GET'])
def jsFile():
   # print('want js')
    r = ''
    with open('Webgraphviz_files/viz.js ') as f:
        r = f.read()
    return r

@app.route('/post_test',methods=['POST','GET'])# 前端向后端发送要执行的源代码时，URL为 post_test 对应着前端 post 时候指定的 url
def get_tasks():
    if request.method == 'POST':
        code = request.get_json(force=True)['code']# 前端那边采用json 格式,前端穿过来的数据指定放在了 'code' 关键字对应的值里
        # 将前端传来的python 程序保存并执行
        with open('code.py','w',encoding='utf8') as f:
            f.write(code)
        # 运行浏览器发来的 python 程序
        #proc = subprocess.Popen(['python', 'code.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #consoleOutput = proc.communicate()[0]# 该程序在控制台的所有输出
        # 希望这里运行相应的浏览器提供的程序，然后运行结束，生成 graph 文件
        # 当然，如果是手动，不是自动执行，那当然不必要这一步骤，只要定死读取 graph 文件就 ok 了， 至于 graph 文件的更新，就不是这里的事情了
        
        with open('input.txt') as f:# 对 input.txt 进行格式化，使之符合 graphviz 的图格式
            lines = f.readlines()
            graph = "digraph {"
            for line in lines:
                r = line.strip().split(',')
                if '->' in r[0]: graph+="\n"+r[0]+' '+'[label = '+r[1]+"]\n"
                else: graph+="\n"+r[0]+' '+'[label = '+r[1]+']\n'
            graph+="}"
            with open("graph","w") as out: # 将格式化完毕的图格式数据保存到 graph 文件中
                out.write(graph)
            
        with open('graph','r') as f:# 将图读出来
            graph = f.read()
        return graph# 将图数据返回给前端 
        
    return hello_world()
 
if __name__ == '__main__':
    app.run(host='111.186.1.46',port='2333')

        
            
    