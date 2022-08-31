from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL
)

from settings import (
    ORIGINAL_LENGTH, SHORT_ID_MAX_LENGTH,
    SHORT_ID_ALLOWED_CHARACTERS
)

REQUIRED_FIELD = 'Обязательное поле.'
INCORRECT_LINK = 'Некорректная ссылка.'
WRONG_SIZE = 'Превышено допустимое количество символов.'
WRONG_CHARACTER_SET = 'Использованы недопустимые символы.'

ORIGINAL_LINK_MESSAGE = 'Длинная ссылка'
CUSTOM_ID_MESSAGE = 'Ваш вариант короткой ссылки'
SUBMIT_MESSAGE = 'Добавить'


class UrlForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_MESSAGE,
        validators=[
            DataRequired(message=REQUIRED_FIELD),
            URL(message=INCORRECT_LINK),
            Length(max=ORIGINAL_LENGTH)
        ]
    )
    custom_id = URLField(
        CUSTOM_ID_MESSAGE,
        validators=[
            Length(
                max=SHORT_ID_MAX_LENGTH,
                message=WRONG_SIZE
            ),
            Regexp(
                SHORT_ID_ALLOWED_CHARACTERS + '+$',
                message=WRONG_CHARACTER_SET
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_MESSAGE)
