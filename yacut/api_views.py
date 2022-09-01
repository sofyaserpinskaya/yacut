from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import GenerateShortIdError, URL_map


NO_DATA_ERROR = 'Отсутствует тело запроса'
NO_URL_ERROR = '\"url\" является обязательным полем!'
NO_ID_ERROR = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_DATA_ERROR)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_ERROR)
    original = data['url']
    try:
        if 'custom_id' not in data:
            url_map = URL_map.create(original, validate=True)
        else:
            url_map = URL_map.create(original, data['custom_id'], validate=True)
    except (ValueError, GenerateShortIdError) as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.get_url_map(short_id)
    if url_map is None:
        raise InvalidAPIUsage(NO_ID_ERROR, 404)
    return {'url': url_map.original}, 200
