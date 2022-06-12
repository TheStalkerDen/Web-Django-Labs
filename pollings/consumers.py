import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PollingsConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = "common"

    def connect(self):
        self.accept()
        print(self.scope["user"])
        print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if data["type"] == "added_new_question":
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "added_new_question",
                    "message": data["message"],
                    'sender_channel_name': self.channel_name
                }
            )
        elif data["type"] == "deleted_question":
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "deleted_question",
                    "message": data["message"],
                    'questionId': data["questionId"],
                    'sender_channel_name': self.channel_name,
                }
            )
        elif data["type"] == "vote_for_answer":
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "vote_for_answer",
                    "message": data["message"],
                    'answerId': data["answerId"],
                    'questionId': data["questionId"],
                    'sender_channel_name': self.channel_name,
                }
            )

    def disconnect(self, code):
        print(self.scope["user"])
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def added_new_question(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    def deleted_question(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))

    def vote_for_answer(self, event):
        if self.channel_name != event['sender_channel_name']:
            self.send(text_data=json.dumps(event))
