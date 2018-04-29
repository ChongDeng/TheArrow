import os
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/create_db')
def create_db():
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

    return "success"

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True) 启动调试！！！！！ 一定不能用于生产环境中，因为用户会在错误的页面中执行python程序来黑客你


