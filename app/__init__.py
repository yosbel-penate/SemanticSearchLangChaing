from flask import Flask

UPLOAD_FOLDER = 'store'

app = Flask('app')


from app.router.main_routes import main_bp

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)