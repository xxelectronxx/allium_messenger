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
        self.service_name = '7tcowwy2zjdfed4vdmooh2267i2qxzgw6jldgky7rmhnpoaxth5wahad.onion'
        return self.service_name

    def create_service(self):
        logger.info(" * Getting controller")
        self.controller = Controller.from_port(address=self.host, port=self.control_port)
        try:
            self.controller.authenticate(password="test_password")
            self.controller.set_options([
                ("HiddenServiceDir", self.hidden_svc_dir),
                ("HiddenServicePort", "80 %s:%s" % (self.host, str(self.port)))
            ])
            svc_name = self.get_service_name()
            logger.info(" * Created host: %s" % svc_name)
        except Exception as e:
            print(e)
            logger.info(f'OHMYGOD!!!! {e}')
        self.app.run()


if __name__ == "__main__":
    my_connection = AlliumConnection(hidden_svc_dir='hidden_service')
    my_connection.create_service()
