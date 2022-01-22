import json
import os
import tempfile
import logging
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