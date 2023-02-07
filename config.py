from os import getenv
from dotenv import load_dotenv

load_dotenv()

get_queue = {}


API_ID = int(getenv("API_ID", "13600724")) 
API_HASH = getenv("API_HASH", "ee59fd28d0d065c6b7d105082c6a0ba0")
ASS_HANDLER = list(getenv("ASS_HANDLER", ".").split())
BOT_TOKEN = getenv("BOT_TOKEN","6131058279:AAECPo-81O0XIpN1fItHEuY9wpzgRwxOQKU")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "150"))
LOGGER_ID = int(getenv("LOGGER_ID","-1001523603001"))
MONGO_DB_URI = getenv("MONGO_DB_URI","mongodb+srv://sarcasticboy:sarcasticboy505@cluster0.bv22u.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6033864054").split()))
PING_IMG = getenv("PING_IMG", "https://te.legra.ph/file/d8873018356b2a8a2d4f4.jpg")
START_IMG = getenv("START_IMG","https://te.legra.ph/file/22481327e5f0a8847cc4a.jpg")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/topperbothub")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/clickhereop")
STRING_SESSION = getenv("STRING_SESSION", "BQA1ixueTUsJaCm7mfZwN8uPJMA-fLnTlksqbeiUBKM_BROMQFiOXW73sfFjEZ3WCvBoULmI7NNXEkyMI-keS5VuZ9MuuGL8E8rAR_jm8MRQb9Frd6UtPeADoVF3_WQtQa9kYR6X3FG3CMPK_e0c6gRpvHT9EuR0uVvGz97WbOV3xPMwepSV_grJjrS6ICxzLEP-s_n3ftnIvEL09ZIzBXax2Ez1kksyz1DiI8_4ppmYHNGQNk3MHro9tecDt1CyhafW-iLxBcAxHYidoKO10Karg-bZ2D2W2qRa4vyC9k9Cdy3Tjio0JS-l4bPyb23AxuI0twttcHTJ_fmkRA0a2XzzAAAAAUokJDQA")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "5938660179").split()))
