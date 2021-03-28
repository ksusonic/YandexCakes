SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/cakes'  # TODO: get from environment
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLAlCHEMY_ECHO = False

DEBUG = True

desc = """Чтобы немного скрасить жизнь на самоизоляции, представляем вам интернет-магазин по доставке конфет \
"Сласти от всех напастей". Это REST API сервис, который позволяет нанимать курьеров на работу, \
принимать заказы и оптимально распределять заказы между курьерами, попутно считая их рейтинг и заработок."""
