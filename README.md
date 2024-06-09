# Daily-Japanese-Word
Daily Japanese Word is a web server made using Flask on Python that prompts a different word every day, with its wrinting, pronunciation in hiragana and its meaning. Its implemented in a way that you can adjust word to your japanese level. For example, if you don't know all hiragana characters, you can adjust the daily word reading in order to only get those word you can already read.
![imagen](https://github.com/AlbertoN97/Daily-Japanese-Word/assets/91640565/3343cbf2-54aa-45e7-9dfe-e200c5333711)


## How to configure it?
You will have to edit the code according to your necesities.

**Japanese level of the word that will be generated. From jlpt-n5 (most basic vocabulary) to jlpt-n1 (high japanese level vocabulary).**
level = 'jlpt-n5'

**IP or hostname of the host that will host the server. You will access to the web using that IP/hostname + port**
host = '127.0.0.1'

**Port of the web server**
port = 5000

**Higarana characters: You can remove Hiragana characters in order to avoid certain characters to be used to find new words. You can do it deleting those characters from the list or commenting via # in the python script "server.py"**
    syllables = ["あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
                 "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
                 "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
                 "ま", "み", "む", "め", "も", "や", "ゆ", "よ",
                 "ら", "り", "る", "れ", "ろ", "わ", "を", "ん"]


## Run server
### Requierements:
- Python3
Also you will need to install the following libraries using the following command:
- requests
- flask
- apscheduler
- python-dateutil
        pip install requests flask apscheduler python-dateutil

Then you can run the server with the following command:
        python3 server.py
It will generate a json file which contains the daily word. If the word already exists, it will replace its content the next day.
