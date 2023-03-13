from json import load

with open('D:/GitHub/.misc/tokens.json', 'r') as f:
    doc = load(f)
    
    bot_token = doc["bot-token"]
    db_token = doc["db-token"]