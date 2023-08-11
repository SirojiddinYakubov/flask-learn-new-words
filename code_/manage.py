from code_ import app
from code_.app.core.config import config


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=config.FLASK_DEBUG)
