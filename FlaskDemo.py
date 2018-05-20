import parser

import os
from threading import Thread

from flask import Flask, json, request, jsonify, redirect, render_template, url_for, session, flash, make_response
from flask_restful import reqparse, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I dont\'t know what is pwd'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = '最帅的人 Chong Deng <854143470@qq.com>'
app.config['MAIL_SUBJECT_PREFIX'] = '以帅之名'

from flask_mail import Mail, Message
mail = Mail(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask_moment import Moment
moment = Moment(app)


from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<SCUT Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<SCUT User %r>' % self.username


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


#####################################  json request2
#访问方式：
# curl -d {\"Command\":1,\"MPId\":\"5555\",\"Pin\":\"3434\",\"title\":\"test\"}
# -H "Content-Type: application/json"  http://127.0.0.1:5000/json_url2
@app.route('/json_url2', methods=['POST'])
def json_url2():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    return jsonify({'task': task}), 201


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

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

#####################################  error json
@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


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

#####################################  web form test

@app.route('/web_form', methods=['GET', 'POST'])
def web_form_test():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@app.route('/web_form2', methods=['GET', 'POST'])
def web_form_test2():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('web_form_test2'))
    return render_template('index.html', form=form, name=session.get('name'))


class CustomForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/web_form3', methods=['GET', 'POST'])
def web_form_test3():
    form = CustomForm()
    if form.validate_on_submit():
        session['name'] = form.username.data
        return redirect(url_for('web_form_test3'))
    return render_template('custom_form.html', form=form, name=session.get('name'))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(5, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')

@app.route('/web_form4', methods=['GET', 'POST'])
def web_form_test4():
    form = LoginForm()
    if form.validate_on_submit():
        print("role:", form.role.data)
        session['name'] = form.email.data
        return redirect(url_for('scut_success'))
    return render_template('custom_form2.html', form=form, name=session.get('name'))


@app.route('/wtf_form', methods=['GET', 'POST'])
def wtf_form_test():
    from scut_forms import AdminProfileForm
    form = AdminProfileForm()
    if form.validate_on_submit():
        print("date: ", form.birthday.data)
        return redirect(url_for('scut_success'))
    return render_template('custom_form.html', form=form)

@app.route('/scut_success')
def scut_success():
    return "cool!"

#####################################  flash test

@app.route('/flash', methods=['GET', 'POST'])
def falsh_test():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
            flash('Test!')
        session['name'] = form.name.data
        return redirect(url_for('web_form_test2'))
    return render_template('index.html', form=form, name=session.get('name'))



#####################################  database test
@app.route('/create_db')
def db_test():
    db.create_all()
    return 'hello world'

@app.route('/insert_row')
def insert_row_test():
    db.create_all()
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')

    user_john = User(username='john', role=admin_role)
    user_susan = User(username='susan', role=user_role)
    user_david = User(username='david', role=user_role)

    db.session.add_all([admin_role, mod_role, user_role,
                         user_john, user_susan, user_david])
    db.session.commit()
    # following line will invoke error!
    #return admin_role.id + ", " + mod_role.id + ", " + user_role.id
    return "success"

@app.route('/db_query1')
def db_query_test1():
    #1 取回模型对应表中的所有记录：
    RoleList = Role.query.all()
    for RoleItem in RoleList:
        print("get all result:" , RoleItem)

    return "success"

@app.route('/db_query2')
def db_query_test2():
    # 1 取回username='john'的所有记录：
    print(str(User.query.filter_by(username='john')))
    for UserItem in User.query.filter_by(username='john').all():
        print("get specified result:", UserItem)

    return "success"

@app.route('/db_query3')
def db_query_test3():
    print(str(User.query.filter_by(username='john', role_id=1)))
    for UserItem in User.query.filter_by(username='john', role_id=1).all():
        print("get specified result:", UserItem)
    return "success"


@app.route('/db_query4')
def db_query_test4():
    # 1 取回name='john'的所有记录; 因为表users没有字段name,只有字段username，所以下面代码报错
    print(str(User.query.filter_by(name='john')))
    for UserItem in User.query.filter_by(name='john').all():
        print("get specified result:", UserItem)

    return "success"

@app.route('/db_query5')
def db_query_test5():
    #多表的关联查询: 查找角色为"User" 的所有用户：
    user_role = Role.query.filter_by(name='User').first()

    print(str(User.query.filter_by(role=user_role)))
    for UserItem in User.query.filter_by(role=user_role).all():
        print("get specified result:", UserItem)

    return "success"


@app.route('/modify_db')
def modify_db():
    for UserItem in User.query.all():
        if UserItem.username == 'john' :
            print("get specified result:", UserItem)
            UserItem.username = 'hanleilei'
            db.session.add(UserItem)
            db.session.commit()

    return "success"


@app.route('/mail')
def mail_test():
    msg = Message(subject = "Hello World!",
                  sender = app.config['MAIL_SENDER'],
                  recipients = ['fqyyang@gmail.com'])
    msg.body = 'hey man, how are you'
    msg.html = '<b>嘿嘿</b>'

    mail.send(msg)

    return "success"

def send_email(to, subject, template, **kwargs):
    if isinstance(to, list):
        print("send email to multiple receipients")
        msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + '-' + subject,
                      sender=app.config['MAIL_SENDER'], recipients=to)
    else:
        print("send email to on receipient")
        msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + '-' + subject,
                      sender=app.config['MAIL_SENDER'], recipients=[to])

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    print("basedir: " , basedir)
    with app.open_resource("static/images/sex.jpg") as fp:
        msg.attach("heihei.jpg", "images/jpg", fp.read())

    with app.open_resource("static/video/heihei.mp4") as fp:
        msg.attach("喜欢吗.mp4", "video/mp4", fp.read())

    # Attachments = ['static\images\sex.jpg', 'static\\video\heihei.mp4']
    # Attachments = ['static\images\sex.jpg']
    # for f in Attachments:
    #     if ".jpg" in f:
    #         ContentType = "images/jpg"
    #     elif  ".mp4" in f:
    #         ContentType = "video/mp4"
    #
    #     with app.open_resource(f) as fp:
    #         msg.attach(filename = os.path.join(basedir, f), data=fp.read(),
    #                    content_type = ContentType)
            # msg.attach(filename= os.path.join(basedir, f), data=fp.read(),
            #            content_type='application/octet-stream')

    mail.send(msg)

@app.route('/mail2', methods=['GET', 'POST'])
def mail2():
    send_email(['fqyyang@gmail.com', 'nan.ding@gmail.com'], '代码测试：周末出来吃饭',
               'mail/lunch', time='04/29/2018 12:00:00')

    # send_email('420378081@qq.com', '代码测试：周末出来吃饭',
    #            'mail/lunch', time='04/29/2018 12:00:00')

    return "success"



@app.route('/async_email')
def async_email_test():
    send_email2(['fqyyang@gmail.com', 'nan.ding@gmail.com'], '代码测试：异步发送邮件 周末出来吃饭',
               'mail/lunch', time='04/29/2018 12:00:00')
    return "success"

def send_email2(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + '-' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=to)

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#####################################  httpauth test

# from flask_httpauth import HTTPBasicAuth
# auth = HTTPBasicAuth()
#
# @auth.get_password
# def get_password(username):
#     if username == 'scut':
#         return '401'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)
#
# @app.route('/credential', methods=['GET'])
# @auth.login_required
# def login():
#     return jsonify({'log in result': "success"})


#####################################  httpauth test2
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username != 'scut' or password != '401':
        return False

    return True

@auth.error_handler
def unauthorized():
    return make_response(jsonify({ 'login': 'failure'}), 403)

@app.route('/auth2')
@auth.login_required
def auth2_func():
    return jsonify({ 'login': 'success' })



#####################################  upload

@app.route('/upload')
def upload_func():
    return render_template('upload.html')

#####################################  upload 2
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#将上传文件限制为最大 32 MB 。 如果请求传输一个更大的文件， Flask 会抛出一个RequestEntityTooLarge异常
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app_dir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            upload_dir = os.path.join(app_dir, app.config['UPLOAD_FOLDER'])
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            uploaded_file = request.files['file']

            fname = secure_filename(uploaded_file.filename)
            print('file name is %s' % fname)
            uploaded_file.save(os.path.join(upload_dir, fname))  # 保存文件到upload目录

            flash("upload successfully!")
            return redirect(url_for('upload2'))
    return render_template('upload2.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True) 启动调试！！！！！ 一定不能用于生产环境中，因为用户会在错误的页面中执行python程序来黑客你


