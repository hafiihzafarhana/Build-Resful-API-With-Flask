from flask import Flask, jsonify
import os

# berisi kode untuk membuat dan mengonfigurasi objek aplikasi Flask, dan mungkin mendaftarkan blueprint atau modul lain yang relevan dengan aplikasi ini.


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY")
        )

    else:
        app.config.from_mapping(
            test_config
        )

    @app.get("/")
    def index():
        return "Hai"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
