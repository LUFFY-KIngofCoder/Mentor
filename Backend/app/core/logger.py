import logging
import json
from datetime import datetime
from contextvars import ContextVar

# This is our "magic" storage for the request ID
request_id_var: ContextVar[str] = ContextVar("request_id", default="system")

class JSONFormatter(logging.Formatter):
    def format(self, record):
        # Every time someone logs something, we intercept it and build a JSON dictionary
        log_obj = {
            "timestamp": datetime.now().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": request_id_var.get(),
            "logger": record.name,
        }
        return json.dumps(log_obj)

def setup_logger():
    logger = logging.getLogger("mentor")
    logger.setLevel(logging.INFO)
    
    # Attach our custom JSON Formatter to the console output
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        logger.addHandler(console_handler)
        
    return logger
# Export the logger so other files can import it!
logger = setup_logger()

    