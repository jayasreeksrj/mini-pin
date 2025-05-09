
from flask import request, redirect, render_template
from common_lib.common.shortener import generate_slug

def init_routes(app, url_store, logger):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        short_url = None
        if request.method == 'POST':
            long_url = request.form['url']
            slug = generate_slug()
            url_store[slug] = long_url
            short_url = f"/go/{slug}"
            logger.info(f"Shortened {long_url} to {short_url}")
        return render_template('index.html', short_url=short_url)

    @app.route('/go/<slug>')
    def go(slug):
        if slug in url_store:
            return redirect(url_store[slug])
        return "Invalid short URL", 404
