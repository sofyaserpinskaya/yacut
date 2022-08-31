from flask import abort, flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import URL_map


GENERATE_SHORT_ID_ERROR = 'Не удалось сгенерировать короткую ссылку.'
SHORT_ID_NAME_ERROR = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if form.custom_id.data == '' or form.custom_id.data is None:
        short_id = URL_map().get_unique_short_id()
        if short_id is None:
            flash(GENERATE_SHORT_ID_ERROR)
    else:
        short_id = form.custom_id.data
        if URL_map().get_url_map(short_id) is not None:
            flash(
                SHORT_ID_NAME_ERROR.format(short_id),
            )
            return render_template('index.html', form=form)
    url_map = URL_map.create_from_form(form.original_link.data, short_id)
    return render_template('index.html', form=form, url_map=url_map)


@app.route('/<short_id>', methods=['GET'])
def get_original_url(short_id):
    url_map = URL_map().get_url_map(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)


if __name__ == '__main__':
    app.run()
