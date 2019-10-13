from flask import Response
import yaml
import logging

from viberbot import Api

from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

secrets = yaml.safe_load(open("secrets.yml"))
logger = logging.getLogger("VibeMachine")

class VibeMachine(Api):

    def __init__(self, bot_configuration=None):
        if not bot_configuration:
            bot_configuration = BotConfiguration(
            name='VibeMachine',
            avatar='https://cdn.vox-cdn.com/thumbor/HftXuxUl3QZUjm9Hxjr9I9BQGUw=/0x0:570x375/1820x1213/filters:focal(240x143:330x233):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/62359567/slack_imgs_2.0.jpg',
            auth_token=secrets['vibemachine_auth_token']
        )
        super().__init__(bot_configuration)
    
    def deal_with_message(self, request):
        if not self.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
            return Response(status=403)
        # this library supplies a simple way to receive a request object
        viber_request = self.parse_request(request.get_data())

        if isinstance(viber_request, ViberMessageRequest):
            message = viber_request.message
            # lets echo back
            self.send_messages(viber_request.sender.id, [
                message
            ])
        elif isinstance(viber_request, ViberSubscribedRequest):
            viber.send_messages(viber_request.get_user.id, [
                TextMessage(text="thanks for subvibing!")
            ])
        elif isinstance(viber_request, ViberFailedRequest):
            logger.warning("vibe machine broke. failure: {0}".format(viber_request))

        return Response(status=200)        