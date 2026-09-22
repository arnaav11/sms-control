import threading

from queue import Queue
from flask import Flask, request, jsonify

class SMSListener:
    def __init__(self, data_queue: Queue, port: int = 8008):
        self.app = Flask(__name__)
        self.queue = data_queue
        self.port = port

        self.app.add_url_rule('/api', view_func=self.handle_post, methods=['POST'])

    def handle_post(self):
        data = request.get_json() or request.form.to_dict()
        
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        self.queue.put(data)
        
        return jsonify({"status": "success", "message": "Data received and queued"}), 200

    def start(self):
        server_thread = threading.Thread(
            target=self.app.run, 
            kwargs={"host": "0.0.0.0", "port": self.port, "debug": False, "use_reloader": False},
            daemon=True
        )
        server_thread.start()