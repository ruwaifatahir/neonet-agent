from dotenv import load_dotenv
import os
from exa_py import Exa

load_dotenv()

exa = Exa(api_key = os.getenv("EXA_API_KEY"))