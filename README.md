# Chinese Handwriting Anki Deck Generator
This is a project to create Anki flashcard decks using the CASIA Chinese handwriting database. These decks can be used to learn how to recognize Chinese handwriting.

### Usage
`from main import create_deck`

`create_deck(name, character_list=None, example_count=30)`
where `name` is the name of the deck to create, `character_list` is a list of characters to include in the deck, and `example_count` is the number of examples to use.
By default, creates 30 examples of every character.
Example code to create decks for all HSK lists can be found in `main.py`.

##### Ideas
* HSK Lists
* Your textbook of choice
* The characters you already know
* Any list of characters you might need to see written.

##### Anki
Anki is an open source flashcard program. [Find out more here.](https://apps.ankiweb.net/)

##### CASIA
Casia is a research database containing many images of native Chinese handwriting. [Find out more here](http://www.nlpr.ia.ac.cn/databases/handwriting/Home.html).

### Current status
First release available. Testing has been limited, use at your own risk. Unfortunately limited to simplified characters.

### Copyright warning
We are currently pending approval from the CASIA researchers. Until then, do not distribute any data, whether in flashcards or other form, without express written permission from the CASIA team.
