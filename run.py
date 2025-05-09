import sys
import os

# Get the absolute path to the common-lib directory
common_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'common-lib'))
sys.path.insert(0, common_lib_path)

from flask import Flask
from app.routes import init_routes
from common.logger import setup_logger
from common.shortener import generate_slug

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Set up the logger
logger = setup_logger()

# Initialize a dictionary to store URLs
url_store = {}

# Initialize routes from the routes.py file
init_routes(app, url_store, logger)

# Start the application
if __name__ == '__main__':
    logger.info("Starting Mini-Pin App")
    app.run(host='0.0.0.0', debug=True)