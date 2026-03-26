from typing import List, Dict, Any
from datetime import datetime
import json
import os

class LogManager:
    def __init__(self, log_file: str = "logs/gateway_logs.json"):
        self.logs = []
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self._load_logs()
    
    def _load_logs(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.logs = json.load(f)
            except:
                self.logs = []
    
    def _save_logs(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.logs[-1000:], f)
    
    def log_request(self, **kwargs):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            **kwargs,
            'prompt_snippet': kwargs['prompt'][:100] + '...' if len(kwargs['prompt']) > 100 else kwargs['prompt']
        }
        self.logs.append(log_entry)
        self._save_logs()
    
    def get_logs(self, limit: int = 100):
        return self.logs[-limit:][::-1]