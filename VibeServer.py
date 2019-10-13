from flask import Flask, request
from VibeMachine import VibeMachine
# from pyngrok import ngrok
import logging
import yaml

import time
import sched
import threading

app = Flask(__name__)
logger = logging.getLogger("VibeServer")
secrets = yaml.safe_load(open("secrets.yml"))
vm = VibeMachine()

@app.route('/', methods=['POST'])
def incoming():
    logger.debug("POST request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    try:
        return vm.deal_with_message(request)
    except Exception:
        return Response(status=420)

@app.route('/', methods=['GET'])
def home():
    logger.debug("GET request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    return 'Hello, World!'

def set_webhook(viber, url):
	viber.set_webhook(url)


if __name__ == "__main__":
    try:
        logger.info("Logging")
        # ngrok.set_auth_token(secrets['ngrok_auth_token'])
        
        #public_url = ngrok.connect(5050)
        #public_url = public_url.replace("http", "https")
        public_url = "https://73a39273.ngrok.io"
        logger.info("Ngrok tunnel at: %s" % public_url)

        print("here?")
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(5, 1, set_webhook, (vm,public_url,))
        t = threading.Thread(target=scheduler.run)
        t.start()
        #context = ('server.crt', 'server.key')
        app.run(host='127.0.0.1', port=8080, debug=True) #, ssl_context=context)
        logger.info("Running")
    except Exception as e:
        print(e)
    finally:
        pass
        #ngrok.disconnect(public_url)