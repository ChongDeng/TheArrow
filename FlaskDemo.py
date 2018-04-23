import parser
from flask import Flask, json, request, jsonify, redirect, render_template, url_for
from flask_restful import reqparse, abort

app = Flask(__name__)

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)

#默认为get方法！！！
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

@app.route("/scut_type/<int:age>")
def scut_with_para_type(age):
    obj = {'age': age, "msg": 'hello'}
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

#####################################  post request

#访问方式： curl -X POST http://127.0.0.1:5000/scut_post
@app.route('/scut_post', methods=['POST'])
def scut_post():
    return 'hello post'


"""
 test4:
    curl -X POST    http://127.0.0.1:5000/index/nidaye
    curl -X GET     http://127.0.0.1:5000/index/nidaye
    curl -X PUT     http://127.0.0.1:5000/index/nidaye
    curl -X DELETE  http://127.0.0.1:5000/index/nidaye

 """
@app.route('/index/<user>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def http_all(user):
    return 'index %s' % user


#访问方式： curl 127.0.0.1:5000/user  -d "name=chongdeng&rate=99&other=1&bar=yes" -X POST
@app.route('/user', methods=['POST'])
def user():
    parser = reqparse.RequestParser()
    parser.add_argument('rate', type=int, help='Rate to charge for this resource')
    parser.add_argument('name', type=str, required=True)
    args = parser.parse_args()
    user = {'rate' : args.get('rate'), 'name': args['name']}
    return json.dumps(user)

#####################################  json request

#访问方式：
# curl -d {\"Command\":1,\"MPId\":\"5555\",\"Pin\":\"3434\",\"MobileReqId\":\"123\"}
# -H "Content-Type: application/json"  http://127.0.0.1:5000/json_url
@app.route('/json_url', methods=['POST'])
def json_url():
    data = request.data.decode('utf-8')

    # convert request data string to json
    ScutJson = json.loads(data)
    ScutJson["result"] = 0
    print(ScutJson)

    # convert json to utf8
    # method 1 : return jsonify(ScutJson)
    # method 2
    return json.dumps(ScutJson,ensure_ascii=False).encode('utf8')

 #####################################  request object
@app.route('/request')
def request_test():
    print (app.url_map)
    return "yes"


 #####################################  response
@app.route('/bad_response')
def bad_response_test():
    return '<h1>Bad Request</h1>', 400


 #####################################  redirect
@app.route('/redirect_test')
def redirect_test():
    return redirect('http://www.baidu.com')


@app.route('/user/<id>')
def get_user(id):
    if id != 5:
        print("will abort now!")
        abort(404)
    print("this line will not be invoked!")
    return '<h1>This will also not be invoked!</h1>'

#####################################  render

@app.route('/render1')
def render1():
    return render_template('index.html')

@app.route('/render2/<name>')
def render2(name):
    return render_template('user.html', name = name + " shit")



#####################################  template inheritance

@app.route('/inherit')
def inherit_test():
    return render_template('scut_base.html')

@app.route('/inherit2')
def inherit_test2():
    return render_template('scut_child.html')

#####################################  bootstrap

@app.route('/bootstrap')
def bootstrap_test():
    return render_template('scut_bootstrap_base.html', name = "Tom")


#####################################  error page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


#####################################  url_for

#访问方式： 1 浏览器中 http://127.0.0.1:5000/query_user?id=5
#          2 advanced rest client中也只能用http://127.0.0.1:5000/query_user?id=5
@app.route('/query2')
def query2():
    id = request.args.get('id')
    return 'query user:' + id

@app.route('/url_for')
def url_for_test():
    return redirect(url_for('query2', id = '5', _external = True))

@app.route("/query3/<name>")
def query3(name):
    obj = {'name': name, "msg": 'hello'}
    res = json.dumps(obj)
    return res

@app.route('/url_for2')
def url_for2_test():
    return redirect(url_for('query3', name = 'hello', _external = True))


#####################################  static

@app.route('/static_test')
def static_test():
    return render_template('404.html'), 404


#####################################  local date and time
@app.route('/local')
def local_test():
    from datetime import datetime
    return render_template('local.html',
                           current_time = datetime.utcnow())

if __name__ == '__main__':
    app.run()
    # app.run(debug=True) 启动调试！！！！！ 一定不能用于生产环境中，因为用户会在错误的页面中执行python程序来黑客你


