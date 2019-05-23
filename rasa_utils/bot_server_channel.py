from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
from datetime import datetime
import json
import logging
import yaml
import rasa_core

from uuid import uuid4
from flask import Blueprint, jsonify, request, Flask, Response, make_response
from flask_cors import CORS

from rasa_core.channels.channel import UserMessage
from rasa_core.channels.channel import InputChannel, OutputChannel
from rasa_core.events import SlotSet

from rasa_core.utils import EndpointConfig
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.run import serve_application
from rasa_core import config
from rasa_core.channels.channel import CollectingOutputChannel
from flask import json
from klein import Klein

def request_parameters(request):
    if request.method.decode('utf-8', 'strict') == 'GET':
        return {
            key.decode('utf-8', 'strict'): value[0].decode('utf-8',
                                                           'strict')
            for key, value in request.args.items()}
    else:
        content = request.content.read()
        try:
            return json.loads(content.decode('utf-8', 'strict'))
        except ValueError as e:
            logger.error("Failed to decode json during respond request. "
                         "Error: {}. Request content: "
                         "'{}'".format(e, content))
            raise


logger = logging.getLogger()


class FileMessageStore:

    DEFAULT_FILENAME = "message_store.json"

    def __init__(self, filename=DEFAULT_FILENAME):
        self._store = defaultdict(list)
        self._filename = filename
        try:
            for k, v in json.load(open(self._filename, "r")).items():
                self._store[k] = v
        except IOError:
            pass

    def log(self, cid, username, message, uuid=None):
        if uuid is None:
            uuid = str(uuid4())
        self._store[cid].append(
            {
                "time": datetime.utcnow().isoformat(),
                "username": username,
                "message": message,
                "uuid": uuid,
            }
        )
        self.save()

    def clear(self, cid):
        self._store[cid] = []
        self.save()

    def save(self):
        json.dump(self._store, open(self._filename, "w"))

    def __getitem__(self, key):
        return self._store[key]


class BotServerOutputChannel(OutputChannel):
    def __init__(self, message_store):
        self.message_store = message_store

    def send_text_message(self, recipient_id, message):
        for message_part in message.split("\n\n"):
            self.message_store.log(
                recipient_id, "bot", {"type": "text", "text": message_part}
            )

    def send_text_with_buttons(self, recipient_id, message, buttons, **kwargs):
        # type: (Text, Text, List[Dict[Text, Any]], **Any) -> None
        """Sends buttons to the output.
        Default implementation will just post the buttons as a string."""

        self.send_text_message(recipient_id, message)
        self.message_store.log(
            recipient_id, "bot", {"type": "button", "buttons": buttons}
        )

    def send_image_url(self, recipient_id, image_url):
        # type: (Text, Text) -> None
        """Sends an image. Default will just post the url as a string."""

        self.message_store.log(
            recipient_id, "bot", {"type": "image", "image": image_url}
        )


class BotServerInputChannel(InputChannel):
    app = Klein()

    def __init__(
        self, agent=None, preprocessor=None, port=5002, message_store=FileMessageStore()
    ):
        logging.basicConfig(level="DEBUG")
        logging.captureWarnings(True)
        self.message_store = message_store
        self.on_message = lambda x: None
        self.cors_origins = [u'*']
        self.agent = agent
        self.port = port
        self.preprocessor = preprocessor

    @classmethod
    def name(cls):
        return "chatroom"

    def blueprint(self, on_new_message):
        bot_server_webhook = Blueprint('bot_server_webhook', __name__)
        CORS(bot_server_webhook)

        @bot_server_webhook.route("/health", methods=["GET"])
        def health():
            return "healthy"

        @bot_server_webhook.route('/webhook/<sender_id>/parse', methods=['GET', 'POST'])
        def parse(self, request, sender_id):
        request.setHeader('Content-Type', 'application/json')
        request_params = request_parameters(request)

        if 'query' in request_params:
            message = request_params.pop('query')
        elif 'q' in request_params:
            message = request_params.pop('q')
        else:
            request.setResponseCode(400)
            return json.dumps({"error": "Invalid parse parameter specified"})
        try:
            response = self.agent.start_message_handling(message, sender_id)
            request.setResponseCode(200)
            return json.dumps(response)
        except Exception as e:
            request.setResponseCode(500)
            logger.error("Caught an exception during "
                         "parse: {}".format(e), exc_info=1)
            return json.dumps({"error": "{}".format(e)})


        @bot_server_webhook.route("/conversations/<cid>/log", methods=["GET"])
        def show_log(cid):
            return json.dumps(self.message_store[cid])

        @bot_server_webhook.route("/conversations/<cid>/tracker", methods=["GET"])
        def tracker(cid):
            if self.agent:
                tracker = self.agent.tracker_store.get_or_create_tracker(cid)
                tracker_state = tracker.current_state(
                    should_include_events=True,
                    only_events_after_latest_restart=True
                )

                return json.dumps(tracker_state)
            else:
                return make_response("Could not access agent", 400)
            
        @bot_server_webhook.route("/conversations/<sender_id>/respond", methods=['GET', 'POST'])
        def respond(self, request, sender_id):
            request.setHeader('Content-Type', 'application/json')
            request.setHeader('Access-Control-Allow-Origin', '*')
            request_params = request_parameters(request)
            if 'query' in request_params:
                message = request_params.pop('query')
            elif 'q' in request_params:
                message = request_params.pop('q')
            else:
                request.setResponseCode(400)
                return json.dumps({"error": "Invalid parse parameter specified"})
            try:
                out = CollectingOutputChannel()
                response = self.agent.handle_message(message, output_channel=out, sender_id=sender_id)
                request.setResponseCode(200)
                return json.dumps(response)
            except Exception as e:
                request.setResponseCode(500)
                logger.error("Caught an exception during "
                            "parse: {}".format(e), exc_info=1)
                return json.dumps({"error": "{}".format(e)})

        return bot_server_webhook
