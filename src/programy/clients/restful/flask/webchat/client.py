import logging

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
from flask import current_app
from programy.clients.client import BotClient
from programy.clients.restful.flask.webchat.config import WebChatConfiguration

class WebChatBotClient(BotClient):

    def __init__(self):
        BotClient.__init__(self, "WebChat")

    def get_description(self):
        return 'ProgramY AIML2.0 Webchat Client'

    def get_client_configuration(self):
        return WebChatConfiguration()


print("Loading, please wait...")
WEBCHAT_CLIENT = WebChatBotClient()

print("Initiating Webchat Client...")
APP = Flask(__name__)

@APP.route('/')
def index():
    return current_app.send_static_file('webchat.html')

# Enter you API keys, here, alternatively store in a db or file and load at startup
# This is an exmaple, and therefore not suitable for production
API_KEYS = [
]

def is_apikey_valid(apikey):
    return bool(apikey in API_KEYS)

@APP.route('/api/v1.0/ask', methods=['GET'])
def ask():

    if WEBCHAT_CLIENT.configuration.client_configuration.use_api_keys is True:
        if 'apikey' not in request.args or request.args['apikey'] is None:
            logging.error("Unauthorised access - api required but missing")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

        apikey = request.args['apikey']
        if is_apikey_valid(apikey) is False:
            logging.error("'Unauthorised access - invalid api key")
            return make_response(jsonify({'error': 'Unauthorized access'}), 401)

    if 'question' not in request.args or request.args['question'] is None:
        print("'question' missing from request")
        logging.error("'question' missing from request")
        abort(400)

    question = request.args['question']

    if 'clientid' not in request.args or request.args['clientid'] is None:
        print("'clientid' missing from request")
        logging.error("'clientid' missing from request")
        abort(400)

    clientid = request.args['clientid']

    userid = request.cookies.get(WEBCHAT_CLIENT.configuration.client_configuration.cookie_id)
    expire_date = None
    if userid is None:
        import uuid
        import datetime

        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=WEBCHAT_CLIENT.configuration.client_configuration.cookie_expires)

        userid = str(uuid.uuid4().hex)
        logging.debug("Setting client cookie to :%s"%userid)
    else:
        logging.debug("Found client cookie : %s"%userid)

    try:
        client_context = WEBCHAT_CLIENT.create_client_context(userid)
        if question == 'YINITIALQUESTION':
            answer = client_context.bot.get_initial_question(userid)
        else:
            answer = client_context.bot.ask_question(userid, question, responselogger=WEBCHAT_CLIENT)

        response_data = {"question": question,
                    "answer": answer,
                    "clientid": clientid
                   }

        response = jsonify({'response': response_data})
        if expire_date is not None:
            response.set_cookie(WEBCHAT_CLIENT.configuration.client_configuration.cookie_id, userid,
                                expires=expire_date)

    except Exception as excep:
        logging.exception(excep)

        response_data = {"question": question,
                    "answer": WEBCHAT_CLIENT.bot.default_response,
                    "clientid": clientid,
                    "error": str(excep)
                   }

        response = jsonify({'response': response_data})
        if expire_date is not None:
            response.set_cookie(WEBCHAT_CLIENT.configuration.client_configuration.cookie_id, userid,
                                expires=expire_date)

    return response

if __name__ == '__main__':

    import signal
    import sys

    def set_exit_handler(func):
        signal.signal(signal.SIGTERM, func)

    def on_exit(sig, func=None):
        print("exit handler triggered")
        sys.exit(1)

    def run():
        print("WebChat Client running on %s:%s" % (WEBCHAT_CLIENT.configuration.client_configuration.host,
                                                   WEBCHAT_CLIENT.configuration.client_configuration.port))
        if WEBCHAT_CLIENT.configuration.client_configuration.debug is True:
            print("WebChat Client running in debug mode")

        if WEBCHAT_CLIENT.configuration.client_configuration.ssl_cert_file is not None and \
           WEBCHAT_CLIENT.configuration.client_configuration.ssl_key_file is not None:

            print ("SSL using Cert:%s and Key: %s"%(WEBCHAT_CLIENT.configuration.client_configuration.ssl_cert_file,
                                                    WEBCHAT_CLIENT.configuration.client_configuration.ssl_key_file))
            context = (WEBCHAT_CLIENT.configuration.client_configuration.ssl_cert_file,
                       WEBCHAT_CLIENT.configuration.client_configuration.ssl_key_file)

            print("Webchat Client running in https mode")
            APP.run(host=WEBCHAT_CLIENT.configuration.client_configuration.host,
                    port=WEBCHAT_CLIENT.configuration.client_configuration.port,
                    debug=WEBCHAT_CLIENT.configuration.client_configuration.debug,
                    ssl_context=context)
        else:
            print("Webchat Client running in http mode, careful now !")
            APP.run(host=WEBCHAT_CLIENT.configuration.client_configuration.host,
                    port=WEBCHAT_CLIENT.configuration.client_configuration.port,
                    debug=WEBCHAT_CLIENT.configuration.client_configuration.debug)

    set_exit_handler(on_exit)

    run()
