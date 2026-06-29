import ossapi, os
from dotenv import load_dotenv

load_dotenv()
api = ossapi.Ossapi(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
usuario = os.getenv("USERNAME")
modos = os.getenv("MODOS").split(",")