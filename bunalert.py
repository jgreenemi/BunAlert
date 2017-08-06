import boto3
import logging
from flask import Flask
from flask import request
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

app = Flask(__name__)

# Setup logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/')
def index():
    logging.info('index page started.')
    template = Environment(loader=FileSystemLoader('html/')).get_template('index.j2')
    page = template.render()
    logging.info('index page returned.')
    return page, 200


@app.route('/subscribe', methods=['POST'])
def subscribe():
    logging.info('subscribe page started.')
    try:
        form_response = request.form
        subscriber_number = form_response['subscriber_number']
        if not subscriber_number:
            raise Exception('No subscriber number was passed in!')

        logging.info('subscribe page got valid subscriber_number.')
        # Try to subscribe the number.
        topic_arn = 'arn:aws:sns:us-west-2:277012880214:BunAlert'
        snsclient = boto3.client(
            'sns',
            region_name='us-west-2'
        )

        logging.info('subscribe page made SNS client.')
        subscribe_response = snsclient.subscribe(
            TopicArn=topic_arn,
            Protocol='sms',
            Endpoint='{}'.format(subscriber_number)
        )

        logging.info('subscribe page subscribed the new subscriber_number.')
        # If all's good, render the response page.
        template = Environment(loader=FileSystemLoader('html/')).get_template('subscribe.j2')
        page = template.render(subscriber_number=subscriber_number)
        logging.info('subscribe page returned.')
        return page, 200
    except Exception as e:
        logging.info('subscribe page errored.')
        page = 'Something went wrong! Exception: {}'.format(e)
        logging.error(page)
        return page, 400

if __name__ == '__main__':
    app.run('localhost', '5000')
