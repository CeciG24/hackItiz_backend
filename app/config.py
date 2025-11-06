# app/config.py
import os

class Config: 
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ceciliaga604_db_user:IdN67uuHC44U5r5K@hackathonflights.8nygcts.mongodb.net/vuelosDB?retryWrites=true&w=majority")
