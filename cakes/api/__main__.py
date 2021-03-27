import logging
from aiohttp.web import run_app
from cakes.api.app import create_app


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = create_app()
    run_app(app)


if __name__ == '__main__':
    main()
