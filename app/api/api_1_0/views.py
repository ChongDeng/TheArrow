from flask import render_template

from . import api
@api.route('/kiwi')
def kiwi():
    return render_template('my_bootstrap_test.html')

