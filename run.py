
from flask import Flask
from app.routes import init_routes
from common_lib.common.logger import setup_logger

app = Flask(__name__)
logger = setup_logger()

url_store = {}

init_routes(app, url_store, logger)

if __name__ == '__main__':
    logger.info("Starting Mini-Pin App")
    app.run(debug=True)
