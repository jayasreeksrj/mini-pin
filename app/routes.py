import sys
import os
import re

# Get the absolute path to the common-lib directory
common_lib_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'common-lib'))
if common_lib_path not in sys.path:
    sys.path.insert(0, common_lib_path)

from flask import request, redirect, render_template, url_for
from common.shortener import generate_slug

def is_valid_url(url):
    # Basic URL validation
    pattern = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)', re.IGNORECASE)
    return bool(pattern.match(url))

def init_routes(app, url_store, logger):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        short_url = None
        error = None
        if request.method == 'POST':
            long_url = request.form['url']
            
            # Add http:// if missing
            if not re.match(r'^https?://', long_url):
                long_url = 'http://' + long_url
            
            if is_valid_url(long_url):
                slug = generate_slug()
                url_store[slug] = long_url
                short_url = url_for('go', slug=slug, _external=True)
                logger.info(f"Shortened {long_url} to {short_url}")
            else:
                error = "Invalid URL format. Please enter a valid URL."
                
        return render_template('index.html', short_url=short_url, error=error)

    @app.route('/go/<slug>')
    def go(slug):
        if slug in url_store:
            return redirect(url_store[slug])
        return "Invalid short URL", 404

    @app.route('/debug/<slug>')
    def debug(slug):
        if slug in url_store:
            return f"Stored URL: {url_store[slug]}"
        return "Slug not found", 404
