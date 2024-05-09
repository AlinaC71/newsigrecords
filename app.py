from flask import Flask

# Initialize Flask app
app = Flask(__name__, static_url_path='/static')

# Import routes and models
from . import routes

app.config['TEMPLATES_AUTO_RELOAD'] = True


if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)
    
    
