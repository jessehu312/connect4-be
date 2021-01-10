from flask import Blueprint, render_template, request, send_from_directory

blueprint = Blueprint('home', __name__)

@blueprint.route('/')
def root():
    return render_template("home/index.html")

@blueprint.route('/<path:filename>')
def serve(filename='index.html'):
    return send_from_directory('./app/static', filename=filename)
