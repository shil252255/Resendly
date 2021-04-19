import os
import json
from dotenv import load_dotenv


load_dotenv()

API_ID = os.environ["TG_API_ID_SERG"]
API_HASH = os.environ["TG_API_HASH_SERG"]
SESSION_NAME = os.environ["SESSION_NAME_SERG"]
FROM_CHAT_NAME = json.loads(os.environ["FROM_CHAT_NAME"])
TO_CHAT_NAME = json.loads(os.environ["TO_CHAT_NAME"])

