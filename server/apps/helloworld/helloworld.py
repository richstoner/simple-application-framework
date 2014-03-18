

from flask import Flask
app = Flask(__name__)

 # app.config.from_pyfile('config.py')

# add the celery tasks as an import
import sys
sys.path.append('../../tasks')

from tasks import add
import time
import json

@app.route("/")
def hello():

    result = add.delay(4, 4)

    while not result.ready():
        time.sleep(1)

    print 'You will only see this if you\'re running this as debug'

    return json.dumps(result.info)


def main():
    app.run(debug=True, port=8000, host='0.0.0.0')

if __name__ == '__main__':
    main()