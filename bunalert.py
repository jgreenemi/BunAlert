import boto3
import logging
import phonenumbers
from flask import Flask
from flask import request
from jinja2 import Environment
from jinja2 import FileSystemLoader
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

app = Flask(__name__)

# Setup logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.route('/')
def index():
    """
    This is the main index page function. Nothing fancy here.
    :return: A tuple of an HTML page and an HTTP Status code.
    """
    logging.info('index page started.')
    template = Environment(loader=FileSystemLoader('html/')).get_template('index.j2')
    page = template.render()
    logging.info('index page returned.')
    return page, 200


@app.route('/subscribe', methods=['POST'])
@app.route('/dev/subscribe', methods=['POST'])
def subscribe():
    """
    This is the function for handling subscription requests. It will error clearly if a new phone number wasn't passed
    in when the page was requested.
    :return: A tuple of an HTML page and an HTTP Status code.
    """
    logging.info('subscribe page started.')
    try:
        form_response = request.form
        subscriber_number = form_response['subscriber_number']
        if not subscriber_number:
            raise Exception('No subscriber number was passed in!')

        logging.info('subscribe page checking subscriber_number is valid.')
        # Checking if subscriber_number matches valid format: +18885554444
        carrier._is_mobile(number_type(phonenumbers.parse(subscriber_number)))

        logging.info('subscribe page got valid subscriber_number of {}.'.format(subscriber_number))
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


@app.route('/alert', methods=['GET', 'POST'])
@app.route('/dev/alert', methods=['GET', 'POST'])
def alert():
    """
    This is a function with two responsibilities: for providing the form for publishing a new alert to the SNS Topic,
    and also for confirming that the new alert was published successfully.

    :return: A tuple of an HTML page and an HTTP Status code.
    """
    logging.info('alert page started.')
    if request.method == 'POST':
        logger.info('alert page POST requested.')
        try:
            form_response = request.form
            alert_message = form_response['alert_message']
            if not alert_message:
                raise Exception('No alert message was passed in!')

            logging.info('alert page got an alert_message!')
            # Try to publish that message.
            topic_arn = 'arn:aws:sns:us-west-2:277012880214:BunAlert'
            snsclient = boto3.client(
                'sns',
                region_name='us-west-2'
            )

            snsclient.publish(Message='Bun Alert Update: A Bun has been spotted! {}'.format(alert_message), TopicArn=topic_arn)

            # If all's well, return to the alert page with success message.
            template = Environment(loader=FileSystemLoader('html/')).get_template('alert.j2')
            page = template.render(alert_result='Alert message published successfully!')
            logging.info('alert page returned.')
            return page, 200

        except Exception as e:
            logging.info('alert page errored.')
            page = 'Something went wrong! Exception: {}'.format(e)
            logging.error(page)
            return page, 400
    else:
        # If it's not a POST, must be a GET! Return form page.
        template = Environment(loader=FileSystemLoader('html/')).get_template('alert.j2')
        page = template.render()
        logging.info('alert page returned.')
        return page, 200


if __name__ == '__main__':
    app.run('localhost', '5000')
