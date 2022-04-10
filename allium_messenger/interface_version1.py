from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import pandas as pd
import csv
import threading
import json
from allium_messenger.connection import AlliumConnection
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def process_message_functor(payload):
    decoded = json.loads(payload.decode("utf-8"))

    print("--------------------------------------------------------------")
    print(f"received message from {decoded['address']}:")
    print(f"   {decoded['message']}")
    print("--------------------------------------------------------------")
    return


allium_object = AlliumConnection(hidden_svc_dir='hidden_service', process_message_functor=process_message_functor)

Window.size = (750, 510)
identifier = None
message = None
new_person_popup = Popup()
delete_person_popup = Popup()


class PeopleList(GridLayout):
    contact_info = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        add_person_btn = Button(text="Add Person",
                                size_hint=(1, None),
                                height=(dp(40)),
                                background_normal="",
                                background_color=(.25, .25, .25, 1))
        delete_person_btn = Button(text="Delete Person",
                                   size_hint=(1, None),
                                   height=(dp(40)),
                                   background_normal="",
                                   background_color=(.25, .25, .25, 1))
        add_person_btn.bind(on_press=self.add_person)
        delete_person_btn.bind(on_press=self.delete_person)
        self.add_widget(add_person_btn)
        self.add_widget(delete_person_btn)
        contacts = pd.read_csv("contacts.csv")
        for i in range(len(contacts)):
            self.person_btn = Button(text=f"{contacts['name'].loc[i]}: {contacts['identifier'].loc[i]}",
                                     size_hint=(1, None),
                                     width=(dp(800)))
            self.person_btn.bind(on_press=self.insert_contact_info)
            self.add_widget(self.person_btn)

    def add_person(self, widget):
        global new_person_popup
        new_person_popup = Popup(title="Add Person",
                                 content=NewPerson(),
                                 size_hint=(None, None),
                                 size=(dp(335), dp(290)))
        new_person_popup.open()

    def delete_person(self, widget):
        global delete_person_popup
        delete_person_popup = Popup(title="Delete Person",
                                    content=DeletePerson(),
                                    size_hint=(None, None),
                                    size=(dp(335), dp(290)))
        delete_person_popup.open()

    def insert_contact_info(self, widget):
        self.contact_info = widget.text.split(": ")[1]
        self.parent.parent.children[0].ids.tor_identifier.text = self.contact_info


class MessageInput(GridLayout):
    send_btn_enabled = False
    clear_inputs = StringProperty()

    def send_message(self):
        if self.ids.tor_identifier.text != "" and self.ids.message.text != "":
            # Code for sending message should be triggered here
            global identifier, message
            identifier = self.ids.tor_identifier.text  # Tor identifier that user wants to send message to
            message = self.ids.message.text  # Message from user
            allium_object.send_message(message, identifier)
            self.ids.tor_identifier.text = self.clear_inputs
            self.ids.message.text = self.clear_inputs
            sent_popup = Popup(title='Message',
                               content=Label(text='Message Sent'),
                               size_hint=(None, None), size=(dp(200), dp(200)))
            sent_popup.open()
        else:
            error_popup = Popup(title='Error',
                                content=Label(text='Check Inputs'),
                                size_hint=(None, None), size=(dp(200), dp(200)))
            error_popup.open()


class NewPerson(GridLayout):

    def confirm_person(self):
        global new_person_popup
        with open('contacts.csv', 'a') as file:
            new_person_info = f"\n{self.ids.new_person_name.text},{self.ids.new_person_identifier.text}"
            file.write(new_person_info)
        new_person_popup.dismiss()


class DeletePerson(GridLayout):

    def confirm_delete(self):
        global delete_person_popup
        people = list()
        with open('contacts.csv', 'r') as file:
            for row in csv.reader(file):
                if row[0] != self.ids.delete_person_name.text and row[1] != self.ids.delete_person_identifier.text:
                    people.append(row)
        with open('contacts.csv', 'w', newline='') as file:
            csv.writer(file).writerows(people)
        delete_person_popup.dismiss()


class AlliumApp(App):
    pass


service = threading.Thread(target=allium_object.create_service, args=(), daemon=True)
service.start()
AlliumApp().run()
