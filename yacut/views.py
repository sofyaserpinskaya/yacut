from flask import flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import GenerateShortIdError, URL_map


SHORT_ID_NAME_ERROR = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if not form.custom_id.data:
        try:
            short_id = URL_map.get_unique_short_id()
        except GenerateShortIdError as error:
            flash(str(error))
    else:
        short_id = form.custom_id.data
        if URL_map.get_url_map(short_id) is not None:
            flash(
                SHORT_ID_NAME_ERROR.format(short_id),
            )
            return render_template('index.html', form=form)
    url_map = URL_map.create(form.original_link.data, short_id)
    return render_template('index.html', form=form, url_map=url_map)


@app.route('/<short_id>', methods=['GET'])
def get_original_url(short_id):
    return redirect(URL_map.get_url_map_or_404(short_id).original)


if __name__ == '__main__':
    app.run()
