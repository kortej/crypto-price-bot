import os
from dotenv import load_dotenv

load_dotenv()

CMC_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
CMC_API_KEY = os.getenv("API_TOKEN")


headers = {
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
}