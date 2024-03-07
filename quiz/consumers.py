# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import authenticate, login


class AuthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'login':
            await self.handle_login(data)
        elif data['type'] == 'signup':
            await self.handle_signup(data)

    async def handle_login(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(self.scope['user'],
                            username=email, password=password)

        if user:
            login(self.scope['user'], user)
            await self.send(text_data=json.dumps({'message': 'Login successful'}))
        else:
            await self.send(text_data=json.dumps({'message': 'Invalid login credentials'}))

    async def handle_signup(self, data):
        # Implement your signup logic here
        await self.send(text_data=json.dumps({'message': 'Signup successful'}))
