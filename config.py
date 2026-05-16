import os

class Config:
    API_ID = int(os.getenv("API_ID", 2040))
    API_HASH = os.getenv("API_HASH", 'b18441a1ff607e10a989891a5462e627')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '8699675744:AAEtrLqY_vN4gSLXIw-qVOI6AAPpXtO2pGw')
