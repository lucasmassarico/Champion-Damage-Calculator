from flask import Flask, send_from_directory, render_template
from flask_restful import Api
from resources.calculator import CalculatorAPI
import os

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('cdc.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


api.add_resource(CalculatorAPI, "/calculator")

if __name__ == '__main__':
    app.run(port=5998, debug=True)
