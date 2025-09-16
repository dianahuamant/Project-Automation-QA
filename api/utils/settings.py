from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

API_BASE_URL = os.environ.get("API_BASE_URL")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_ROLE = os.environ.get("ADMIN_ROLE")
ADMIN_FULL_NAME = os.environ.get("ADMIN_FULL_NAME")