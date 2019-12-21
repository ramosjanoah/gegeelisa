from flask import Blueprint
from flask import Flask, render_template, make_response

view_blueprint = Blueprint('view', 'view_blueprint')

@view_blueprint.route('/', methods=['GET'])
def indexNew():
    title = 'Wikipeda Network'
    return render_template('layouts/index.html',
                           title=title)
