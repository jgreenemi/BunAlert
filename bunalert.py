from flask import Flask
from flask import request
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

app = Flask(__name__)


@app.route('/')
def index():
    template = Environment(loader=FileSystemLoader('html/')).get_template('index.j2')
    page = template.render()
    return page, 200


@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        form_response = request.form
        subscriber_number = form_response['subscriber_number']
        if not subscriber_number:
            raise Exception('No subscriber number was passed in!')
        template = Environment(loader=FileSystemLoader('html/')).get_template('subscribe.j2')
        page = template.render(subscriber_number=subscriber_number)
        return page, 200
    except Exception as e:
        page = 'Something went wrong! Exception: {}'.format(e)
        return page, 400

if __name__ == '__main__':
    app.run('localhost', '5000')
