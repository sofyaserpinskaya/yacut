from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URL_map
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        if form.custom_id.data == '' or form.custom_id.data is None:
            short = get_unique_short_id()
        else:
            short = form.custom_id.data
            if URL_map.query.filter_by(short=short).first() is not None:
                flash(
                    f'Имя {short} уже занято!',
                    'url_exists'
                )
                return render_template('index.html', form=form)
        url_map = URL_map(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'url_created')
        return render_template('index.html', form=form, url_map=url_map)
    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def get_original_url(short):
    url_map = URL_map.query.filter_by(short=short).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)


if __name__ == '__main__':
    app.run()
