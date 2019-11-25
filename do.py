# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 23:50:01 2019

@author: jackl
GOAL: 开发一个简陋的python在线运行网站，借助 python 后端框架flask 快速实现后端的简要开发
"""
from flask import Flask, request
import graphviz
import subprocess

app = Flask(__name__)

@app.route('/',methods=['GET'])# tell flask realation between URL and function who deals with the URL
def hello_world():
    r=""
    with open('index.html',encoding="utf8") as f:
        r = f.read() 
        
    return r

def textPreprocess():
    '''
        对原始的 input.txt 文件进行格式化，生成符合规范的 dot 源码
    '''
    with open('input.txt') as f:# 对 input.txt 进行格式化，使之符合 graphviz 的图格式
        lines = f.readlines()
        graph = "digraph {\n"
        r = [0]*2
        for line in lines:
            print(line)
            pos = line.index(',')
            line = line.strip()
            r[0] = line[0:pos]
            r[1] = line[pos+1:]
            if '->' in r[0]: graph+=r[0]+' '+'[label = '+r[1]+"]\n"
            else: graph+=r[0]+' '+'[label = '+r[1]+']\n'
        graph+="}"
        with open("graph.gv","w",encoding="utf8") as out: # 将格式化完毕的图格式数据保存到 graph 文件中
            out.write(graph)
        return 
    
@app.route('/post_test',methods=['POST','GET'])# 前端向后端发送要执行的源代码时，URL为 post_test 对应着前端 post 时候指定的 url
def get_tasks():
    if request.method == 'POST':
        code = request.get_json(force=True)['code']# 前端那边采用json 格式,前端穿过来的数据指定放在了 'code' 关键字对应的值里
        
        # 将前端传来的python 程序保存并执行
        with open('code.py','w',encoding='utf8') as f:
            f.write(code)
  
        # 运行浏览器发来的 python 程序
        # 这个程序应该生成一个 input.txt 文件
        subprocess.Popen(['python', 'code.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        textPreprocess()# 对输入文本进行处理 ,内部指定了对 input.txt 文件进行处理
        graph = graphviz.Source.from_file("graph.gv")# graph.gv 在函数 textPreproces 中产生，它是一个 dot 源码
        graph.format = 'svg'
        svg = graph.pipe().decode('utf-8')# 通过管道，直接得到 graph 这个 dot 对象的 svg 源码
    
        return svg # 将图数据返回给前端 
        
    return hello_world()
 
if __name__ == '__main__':
    app.run(host='localhost',port='2333')

        
            
    