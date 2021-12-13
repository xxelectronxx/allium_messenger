from stem.control import Controller
from flask import Flask
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":

    app = Flask("example")
    port = 5000
    host = "127.0.0.1"
    hidden_svc_dir = "c:/temp/"

    @app.route('/')
    def index():
        return "<h1>Tor works!</h1>"
    print(" * Getting controller")
    controller = Controller.from_port(address="127.0.0.1", port=9151)
    try:
        controller.authenticate(password="")
        controller.set_options([
            ("HiddenServiceDir", hidden_svc_dir),
            ("HiddenServicePort", "80 %s:%s" % (host, str(port)))
            ])
        svc_name = open(hidden_svc_dir + "/hostname", "r").read().strip()
        print(" * Created host: %s" % svc_name)
        logger.info(" * Created host: %s" % svc_name)
    except Exception as e:
        print(e)
        logger.info(f'OHMYGOD!!!! {e}')
    app.run()