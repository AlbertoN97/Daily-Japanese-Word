import requests
import random
from flask import Flask, render_template_string
import datetime
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
level = 'jlpt-n5'
host = '127.0.0.1'
port = 5000
# File to store the word of the day
WORD_FILE = 'word_of_the_day.json'

# Function to get a random word from Jisho
def get_jisho_results(query,level):
    url = f"https://jisho.org/api/v1/search/words?keyword={query}%20%23{level}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener datos de Jisho: {response.status_code}")
        return None

# Function to extract a random word from the results
def generate_random_word():
    syllables = ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
                 "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
                 "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
                 "ま", "み", "む", "め", "も", "や", "ゆ", "よ",
                 "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"]
    random_syllable = random.choice(syllables)
    jisho_data = get_jisho_results(random_syllable,level)

    if jisho_data and 'data' in jisho_data:
        words = jisho_data['data']
        if words:
            random_word = random.choice(words)
            japanese_entries = random_word.get('japanese', [])
            senses = random_word.get('senses', [])
            
            readings_set = set()
            definitions_set = set()
            
            for entry in japanese_entries:
                word = entry.get('word', '')
                reading = entry.get('reading', '')
                readings_set.add(reading)  # Agregar lectura al conjunto

            for sense in senses:
                english_definitions = sense.get('english_definitions', [])
                for definition in english_definitions:
                    definitions_set.add(definition.lower())
            readings = ", ".join(readings_set)
            definitions = ", ".join(definitions_set)
            
            word_data = {
                'word': word,
                'readings': readings,
                'definitions': definitions
            }
            return word_data
    return None

def update_word_of_the_day():
    word = generate_random_word()
    if word:
        # Write the word to the file
        with open(WORD_FILE, 'w') as f:
            json.dump({'date': str(datetime.date.today()), 'word_data': word}, f)

# Initialize the word of the day if the file doesn't exist
if not os.path.exists(WORD_FILE):
    update_word_of_the_day()

# Schedule the word update every day at midnight
scheduler = BackgroundScheduler()
scheduler.add_job(update_word_of_the_day, 'cron', hour=0, minute=0)
scheduler.start()

@app.route('/')
def home():
    # Read the word of the day from the file
    with open(WORD_FILE, 'r') as f:
        data = json.load(f)
        word_data = data['word_data']
        word = word_data['word']
        readings = word_data['readings']
        definitions = word_data['definitions']

    return render_template_string(html_template, word=word, readings=readings, definitions=definitions)

# HTML template to display the result
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Japanese Word of the Day</title>
    <style>
        body {
            color: #eff4f8;
            font-family: Arial, sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start; /* Align content to the top */
            height: 100vh;
            background-color: #0e2f44;
        }
        .content {
            margin-top: 33vh; /* Adjust this value to position content in the first third */
            text-align: center;
        }
        .word {
            font-size: 24px;
            font-weight: bold;
            color: #eff4f8;
        }
        .reading {
            font-size: 18px;
            color: #eff4f8;
        }
        .definition {
            font-size: 18px;
            margin-top: 10px;
            color: #eff4f8;
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Japanese Word of the Day</h1>
        <div class="word">{{ word }}</div>
        <div class="reading">Reading: {{ readings }}</div>
        <div class="definition">Definitions: {{ definitions }}</div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
