import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id


NO_DATA_ERROR = 'Отсутствует тело запроса'
NO_URL_ERROR = '\"url\" является обязательным полем!'
SHORT_NAME_ERROR = 'Указано недопустимое имя для короткой ссылки'
NAME_EXISTS_ERROR = 'Имя "{}" уже занято.'
NO_ID_ERROR = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(NO_DATA_ERROR)
    if 'url' not in data:
        raise InvalidAPIUsage(NO_URL_ERROR)
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    else:
        short = data['custom_id']
        if re.fullmatch(r'[a-zA-Z0-9]{1,16}', short) is None:
            raise InvalidAPIUsage(SHORT_NAME_ERROR)
        if URL_map.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(NAME_EXISTS_ERROR.format(short))
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(NO_ID_ERROR, 404)
    return {'url': url.original}, 200
