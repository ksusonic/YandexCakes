from flask import Flask
from flask_restful import Api
from api.config import configure_app
from api.handlers import couriers

# 3 кита:
app = configure_app(Flask(__name__))
api = Api(app)

api.add_resource(couriers.Courier, '/couriers/<int:courier_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
