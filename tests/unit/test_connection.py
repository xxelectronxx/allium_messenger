import json
import os
import tempfile
import logging
import urllib3
import requests
from types import SimpleNamespace
from allium_messenger.connection import AlliumConnection

logger = logging.getLogger(__name__)


def test_save_service_key():
    my_connection = AlliumConnection(hidden_svc_dir='hidden_service')

    test_result = {
        "service_id": "aaaaa",
        "private_key": "bbbbb"
    }
    test_result = SimpleNamespace(**test_result)
    fd, path = tempfile.mkstemp()
    logger.info(f"temp file: {path}")
    my_connection.service_key_file = path

    my_connection.save_service_key(test_result)
    assert os.path.exists(path)
    with open(path, "r") as _file:
        key_dict = json.load(_file)
    assert "public" in key_dict
    assert test_result.service_id == key_dict["public"]
    assert "private" in key_dict
    assert test_result.private_key == key_dict["private"]
    os.remove(path)


def test_get_request():
    my_object = AlliumConnection(hidden_svc_dir='hidden_service')
    receiver_address, _ = my_object.get_service_name()
    logger.info(receiver_address)
    proxies = {
        'http': 'socks5h://127.0.0.1:9050'
    }

    response = requests.get(f"http://{receiver_address}.onion", proxies=proxies)
    logger.info(f'{response.text.strip()}')
    assert "Tor works!" in response.text


def test_post_request():
    my_object = AlliumConnection(hidden_svc_dir='hidden_service')
    receiver_address, _ = my_object.get_service_name()
    logger.info(receiver_address)
    proxies = {
        'http': 'socks5h://127.0.0.1:9050'
    }

    response = requests.post(f"http://{receiver_address}.onion/allium",
                             proxies=proxies,
                             json={
                                 "address": f"{receiver_address}.onion",
                                 "message": "My awesome second message (using requests library)"

                             },
                             headers={"Content-Type": "application/js"})
    logger.info(f'{response.text.strip()}')
    message = json.loads(response.text)["message"]
    assert message == "My awesome second message (using requests library)"


def test_send_message():
    my_object = AlliumConnection(hidden_svc_dir='hidden_service')
    receiver_address, _ = my_object.get_service_name()
    logger.info(receiver_address)
    sent_message = "hello there"
    response = my_object.send_message(sent_message, receiver_address)
    received_message = json.loads(response.text)["message"]
    assert received_message == sent_message
