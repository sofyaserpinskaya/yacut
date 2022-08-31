from flask import jsonify, request

from settings import ORIGINAL_LENGTH
from . import app
from .error_handlers import InvalidAPIUsage
from .models import URL_map


NO_DATA_ERROR = 'Отсутствует тело запроса'
NO_URL_ERROR = '\"url\" является обязательным полем!'
ORIGINAL_LENGTH_ERROR = 'Недопустимо длинная ссылка. Максимальная длина - {}.'
NO_ID_ERROR = 'Указанный id не найден'
GENERATE_SHORT_ID_ERROR = 'Не удалось сгенерировать короткую ссылку'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_DATA_ERROR)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_ERROR)
    if len(data['url']) > ORIGINAL_LENGTH:
        raise InvalidAPIUsage(ORIGINAL_LENGTH_ERROR.format(ORIGINAL_LENGTH))
    if (
        'custom_id' not in data or
        data['custom_id'] is None or
        data['custom_id'] == ''
    ):
        data['custom_id'] = URL_map().get_unique_short_id()
        if data['custom_id'] is None:
            raise InvalidAPIUsage(GENERATE_SHORT_ID_ERROR)
    url_map = URL_map().validate_and_create(data)
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map().get_url_map(short_id)
    if url_map is None:
        raise InvalidAPIUsage(NO_ID_ERROR, 404)
    return {'url': url_map.original}, 200
