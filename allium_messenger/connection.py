import os
import json
from stem.control import Controller
from flask import Flask, request
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class AlliumConnection:

    def __init__(self, hidden_svc_dir, app_name='example', port=5000, host='127.0.0.1', control_port=9051):
        self.app = Flask(app_name)
        self.port = port
        self.host = host
        self.control_port = control_port
        self.hidden_svc_dir = f"/var/lib/tor/{hidden_svc_dir}"
        self.controller = None
        self.service_name = None
        self.service_key_file = "./service_key.json"
        logger.info(f'service key file: {os.path.abspath(self.service_key_file)}')

        @self.app.route('/')
        def index():
            return "<h1>Tor works!</h1>"

        self.index = index

        @self.app.route('/allium', methods=['POST'])
        def process_request():
            logger.info(request.data)
            return request.data

        self.request = request

    def get_service_name(self):
        """
        check file ./service_key.json, return private and public keys if available, none otherwise
        :param:
        :return:
        """
        public = None
        private = None
        if os.path.exists(self.service_key_file):
            with open(self.service_key_file, "r") as _file:
                try:
                    key_dict = json.load(_file)
                    if "public" in key_dict:
                        public = key_dict["public"]
                    if "private" in key_dict:
                        private = key_dict["private"]
                except:
                    logger.error("Could not read json file")
        return public, private

    def save_service_key(self, result):
        _private = result.private_key
        key_dict = {
            "public": result.service_id,
            "private": _private
        }
        with open(self.service_key_file, "w") as _file:
            json.dump(key_dict, _file)
        return

    def create_service(self):
        logger.info(" * Getting controller")
        self.controller = Controller.from_port(address=self.host, port=self.control_port)
        try:
            self.controller.authenticate(password="test_password")


            public, private = self.get_service_name()
            if public and private:
                logger.info("reusing existing key")
                self.controller.create_ephemeral_hidden_service({80: 5000}, key_type="ED25519-V3", key_content=private)
            else:
                logger.info("creating new key")
                result = self.controller.create_ephemeral_hidden_service({80: 5000})
                public = result.service_id
                self.save_service_key(result)

            svc_name = public
            logger.info(" * Created host: %s" % svc_name)
        except Exception as e:
            print(e)
            logger.info(f'Could not create hidden service: {e}')
        self.app.run()


if __name__ == "__main__":
    my_connection = AlliumConnection(hidden_svc_dir='hidden_service')
    my_connection.create_service()
