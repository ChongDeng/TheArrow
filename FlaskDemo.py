from flask import Flask, json, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/scut')
def hello_world2():
    return '<h1>Hello World!</h1>'

#####################################  parameter

@app.route("/scut/<name>")
def scut_with_para(name):
    obj = {'name': name, "msg": 'hello'}
    res = json.dumps(obj)
    return res


#访问方式：http://127.0.0.1:5000/page/2/total/10
@app.route("/page/<pages>/total/<total>")
def totalPage(pages, total):
    return u'第' + pages + u',共' + total + u'页'


#访问方式： 1 浏览器中 http://127.0.0.1:5000/query_user?id=5
#          2 advanced rest client中也只能用http://127.0.0.1:5000/query_user?id=5
@app.route('/query_user')
def query_user():
    id = request.args.get('id')
    return 'query user:' + id

if __name__ == '__main__':
    app.run()
