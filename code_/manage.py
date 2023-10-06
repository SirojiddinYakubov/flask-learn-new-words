from __init__ import app
from app.core.config import config

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=config.FLASK_DEBUG)
