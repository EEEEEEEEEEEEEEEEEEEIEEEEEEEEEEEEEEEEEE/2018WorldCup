from app import app
from config import Production


if __name__ == '__main__':
    app.config.from_object(Production)
    app.run()