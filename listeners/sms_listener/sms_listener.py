import os
import hmac
import threading

from queue import Queue
from flask.wrappers import Request
from flask import Flask, request, jsonify

from listeners.listener import Listener


class SMSListener(Listener):
    def __init__(self, data_queue: Queue, port: int = 8008, api_env: str = 'SMS_SECRET_KEY'):
        super().__init__()

        self.app = Flask(__name__)
        self.queue = data_queue
        self.port = port
        self.api_env = api_env

        self.app.add_url_rule('/api', view_func=self.handle_post, methods=['POST'])

    def handle_post(self):
        data = request.get_json() or request.form.to_dict()

        if not self.check_auth(request):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        self.queue.put(data)
        
        return jsonify({"status": "success", "message": "Data received and queued"}), 200

    def check_auth(self, request: Request) -> bool:
        if not request.headers.get("X-API-Key"):
            print('\nAPI key not provided for SMS listener. \n')
            return False
        elif not os.getenv(self.api_env):
            print(f'\nEnvironment variable {self.api_env} not set, please set it to the shared API key \n')
            return False
        elif not hmac.compare_digest(request.headers.get("X-API-Key"), os.getenv(self.api_env)):
            print('\nInvalid API key \n')
            return False

        else:
            return True


    def start(self):
        server_thread = threading.Thread(
            target=self.app.run, 
            kwargs={"host": "0.0.0.0", "port": self.port, "debug": False, "use_reloader": False},
            daemon=True
        )
        server_thread.start()