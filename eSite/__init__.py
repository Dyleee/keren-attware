from pprint import pprint
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import jwt_manager
from .models.models import mongo_engine
from .views.home import HomeView

# from .views.flow import FlowView
# from .views.blog import BlogView
# from .views.media import MediaView
# from .views.vendor import VendorView
# from .views.store import StoreView
# from .views.user import UserView
# from .views.orders import OrdersView
# from .views.paystack import PayStackView

from cachetools import TTLCache
import ssl


# Load environment variables
load_dotenv()


class ClassName(object):
    def __init__(self, *args):
        super(ClassName, self).__init__(*args)


def create_app():

    # Create App Instance and config DB
    app = Flask(__name__)

    # app.cache.init_app(app)
    app.config.from_pyfile("settings.py")

    # Your other app configurations

    @app.context_processor
    def inject_global_variables():
        return {
            "DOMAIN_NAME": app.config["DOMAIN_NAME"],
            "COMPANY_NAME": "Keren",
            "CONTACT_EMAIL": app.config["CONTACT_EMAIL"],
            "CONTACT_PHONE": app.config["CONTACT_PHONE"],
            # Add more variables as needed
        }

    # Your view functions and other configurations

    app.db = ClassName()
    app.cache = TTLCache(maxsize=1000, ttl=6 * 60 * 60)

    @app.after_request
    def handle_options(response):
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers[
            "Access-Control-Allow-Origin"
        ] = "http://localhost:5173" # "https://" + app.config["DOMAIN_NAME"] #"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "Content-Type, X-Requested-With, Authorization"

        return response

    CORS(
        app,
        origins="https://" + app.config["DOMAIN_NAME"],
        support_credentials=True,
        allow_headers=["Authorization", "Content-Type"],
    )
    # Register the routes
    HomeView.register(app)
    MediaView.register(app)
    FlowView.register(app)
    BlogView.register(app)
    VendorView.register(app)
    StoreView.register(app)
    UserView.register(app)
    OrdersView.register(app)
    PayStackView.register(app)

    # TransactionsView.register(app, route_base='transactions')

    # Initialize the JWT Managers
    jwt = jwt_manager.JWTManager(app=app)

    # # Initialize Mongo Engine
    mongo_engine.init_app(app=app, config=app.config)
    # app.mail.init_app(app=app)
    pprint(app.url_map)
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain(
    #     "/etc/letsencrypt/live/api.sproutprime.com/fullchain.pem",
    #     keyfile="/etc/letsencrypt/live/api.sproutprime.com/privkey.pem",
    # )

    return app
