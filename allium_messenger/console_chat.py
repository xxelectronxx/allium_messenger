import json
import threading
import sys
import os
import logging
import time
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_dir = os.path.abspath(os.path.dirname(__file__))
_dir = os.path.join(_dir, "../")
_dir = os.path.abspath(_dir)
sys.path.append(_dir)

from allium_messenger.connection import AlliumConnection


def process_message_functor(payload):
    decoded = json.loads(payload.decode("utf-8"))

    print("--------------------------------------------------------------")
    print(f"received message from {decoded['address']}:")
    print(f"   {decoded['message']}")
    print("--------------------------------------------------------------")
    return


def send_loop(connection):
    time.sleep(3)

    while True:
        message = input("Your message: ")

        logger.info(f"{message}, {connection.get_service_name()[0]}")
        connection.send_message(message, connection.get_service_name()[0])


def get_contacts_from_file(filename):
    contacts = pd.read_csv(filename)
    contacts = {row["name"]: row["identifier"] for _,row in contacts.iterrows()}
    logger.info(contacts)

    return contacts


def main():
    contacts_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "contacts.csv")
    contacts = get_contacts_from_file(contacts_file)
    identifiers = {contacts[k]: k for k in contacts}

    my_connection = AlliumConnection(hidden_svc_dir='hidden_service', process_message_functor=process_message_functor)

    try:
        service = threading.Thread(target=my_connection.create_service, args=(), daemon=True)
        service.start()
    except:
        logger.error("Error: unable to start thread")

    logger.info("ready for input loop")
    send_loop(connection=my_connection)


if __name__ == "__main__":
    main()
