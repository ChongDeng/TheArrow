import os
from flask import Flask, g, request, jsonify, url_for, make_response
from flask_restful import abort

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'auth_token_data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# extensions
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<SCUT User %r>' % self.username

# curl  -d {\"username\":\"scut\",\"password\":\"C13\"}
# -H "Content-Type: application/json"  http://127.0.0.1:5000/api/users
@app.route('/api/users', methods = ['POST', 'GET'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }),\
           201, \
           {'Location': url_for('get_user', id = user.id, _external = True)}

@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})



from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

# curl -u wuhan:hubei -i -X GET http://127.0.0.1:5000/api/resource
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'You have no right to access'}), 401)

# curl -s -D - http://localhost:5000 -H 'Content-Type: application/json'
@app.route('/')
def index():
    return '{"status": "OK!"}'

if __name__ == '__main__':
    if not os.path.exists('auth_token_data.sqlite'):
        db.create_all()
    app.run(debug=True)
    # app.run(debug=True) 启动调试！！！！！ 一定不能用于生产环境中，因为用户会在错误的页面中执行python程序来黑客你


