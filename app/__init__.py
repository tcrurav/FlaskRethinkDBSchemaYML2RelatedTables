# app/__init__.py
from flask import Flask
from rethinkdb import RethinkDB
from app.config import Config

r = RethinkDB()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize RethinkDB connection
    r.connect(app.config["RETHINKDB_HOST"], app.config["RETHINKDB_PORT"]).repl()

    with app.app_context():
        # Create database if doesn't exist
        if not r.db_list().contains(app.config["RETHINKDB_DB"]).run():
            r.db_create(app.config["RETHINKDB_DB"]).run()
        
        # Create tables if they don't exist
        tables = ["bicycles", "countries"]
        for t in tables:
            if not r.db(app.config["RETHINKDB_DB"]).table_list().contains(t).run():
                r.db(app.config["RETHINKDB_DB"]).table_create(t).run()

        # Register routes
        from app.routes.countries_routes import main as countries_routes
        app.register_blueprint(countries_routes)
        
        from app.routes.bicycles_routes import main as bicycles_routes
        app.register_blueprint(bicycles_routes)

    return app