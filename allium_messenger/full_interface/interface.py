from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import pandas as pd
import csv

Window.size = (800, 510)
identifier = None
message = None
new_person_popup = Popup()
delete_person_popup = Popup()
delete_message_popup = Popup()
clear_messages_popup = Popup()


class WindowManager(ScreenManager):
    pass


class SendingWindow(Screen):
    pass


class ReceivingWindow(Screen):
    pass


# Sending Messages
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
        self.parent.parent.children[1].children[3].text = self.contact_info


class MessageInput(GridLayout):
    send_btn_enabled = False
    clear_inputs = StringProperty()

    def send_message(self):
        if self.children[3].text != "" and self.children[1].text != "":
            # Code for sending message should be triggered here
            global identifier, message
            identifier = self.children[3].text  # Tor identifier of person user wants to send to
            message = self.children[1].text  # Message user wants to send
            self.children[3].text = self.clear_inputs
            self.children[1].text = self.clear_inputs
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


# Receiving Messages
class MessageList(GridLayout):
    sender_identifier = StringProperty()
    sender_subject = StringProperty()
    sender_message = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        delete_message_btn = Button(text="Delete Message",
                                    size_hint=(1, None),
                                    height=(dp(40)),
                                    background_normal="",
                                    background_color=(.25, .25, .25, 1))
        clear_messages_btn = Button(text="Clear Messages",
                                    size_hint=(1, None),
                                    height=(dp(40)),
                                    background_normal="",
                                    background_color=(.25, .25, .25, 1))
        delete_message_btn.bind(on_press=self.delete_message)
        clear_messages_btn.bind(on_press=self.clear_messages)
        self.add_widget(delete_message_btn)
        self.add_widget(clear_messages_btn)
        messages = pd.read_csv("messages.csv")
        for i in range(len(messages)):
            self.person_btn = Button(text=f"{messages['identifier'].loc[i]}:"
                                          f"\n{messages['message'].loc[i]}",
                                     size_hint=(1, None),
                                     width=(dp(800)))
            self.person_btn.bind(on_press=self.insert_message_info)
            self.add_widget(self.person_btn)

    def delete_message(self, widget):
        global delete_message_popup
        delete_message_popup = Popup(title="Delete Message",
                                     content=DeleteMessage(),
                                     size_hint=(None, None),
                                     size=(dp(335), dp(290)))
        delete_message_popup.open()

    def clear_messages(self, widget):
        global clear_messages_popup
        clear_messages_popup = Popup(title="Clear Message",
                                     content=ClearMessages(),
                                     size_hint=(None, None),
                                     size=(dp(335), dp(200)))
        clear_messages_popup.open()

    def insert_message_info(self, widget):
        self.sender_identifier = widget.text.split(":")[0]
        self.sender_message = widget.text.split(":")[1].strip()
        self.parent.parent.children[1].children[2].text = self.sender_identifier
        self.parent.parent.children[1].children[0].text = self.sender_message


class DeleteMessage(GridLayout):

    def confirm_message_delete(self):
        global delete_message_popup
        messages = list()
        with open('messages.csv', 'r') as file:
            for row in csv.reader(file):
                if row[0] != self.ids.delete_message_identifier.text and row[1] != self.ids.delete_message_content.text:
                    messages.append(row)
        with open('messages.csv', 'w', newline='') as file:
            csv.writer(file).writerows(messages)
        delete_message_popup.dismiss()


class ClearMessages(GridLayout):

    def confirm_message_clear(self):
        global clear_messages_popup
        with open('messages.csv', 'r') as file:
            header = csv.DictReader(file).fieldnames
        with open('messages.csv', 'w', newline='') as file:
            csv.writer(file).writerow(header)
        clear_messages_popup.dismiss()


class MessageInfo(GridLayout):
    pass


# Launch Interface
class AlliumApp(App):
    pass


AlliumApp().run()
