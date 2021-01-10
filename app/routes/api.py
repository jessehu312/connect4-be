from flask import Blueprint
from app import settings

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/client-config')
def client_config():
    return { 
        'radar': settings.RADAR_PUBLISHABLE_KEY
    }