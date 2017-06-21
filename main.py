from collections import defaultdict

import genanki

from casia import CASIA
from hsk import HSK
from models import get_model


def load_data(data, character_list=None, example_count=30):
    deck_data = defaultdict(list)
    media = []

    characters_loaded = 0
    for image, character in data.load_all():

        # Only include requested characters
        if character_list is None or character in character_list:
            # Only include as many examples as requested
            count = len(deck_data[character])
            if count < example_count:
                filename = "%s_%s.jpg" % (character, len(deck_data[character])+1)
                image.save(filename)
                deck_data[character].append(filename)
                media.append(filename)
                characters_loaded = characters_loaded + 1

            # Early stop if you have enough examples
            if characters_loaded >= len(character_list) * example_count:
                if len([character for character in deck_data if len(deck_data[character]) < example_count]) == 0:
                    break

    return deck_data, media

def create_deck(data, deck_id, name, character_list=None, example_count=30):
    # Create deck
    deck = genanki.Deck(deck_id, name)

    # Get data and create media
    deck_data, media = load_data(data, character_list=character_list, example_count=example_count)

    print(media)

    # Create notes
    for character in deck_data:
        note_fields = [character]
        examples = ["<img src=\"%s\">" % image for image in deck_data[character]]
        assert len(examples) == example_count, "Wrong number of examples for %s" % character
        note_fields.extend(examples)
        #print(note_fields)
        my_note = genanki.Note(model=get_model(example_count=example_count), fields=note_fields)
        deck.add_note(my_note)

    # Create the package and output
    package = genanki.Package(deck)
    package.media_files = media
    package.write_to_file('%s.apkg' % name)



def main():
    data = CASIA()
    create_deck(data, 2041831503, "HSK1", character_list=HSK["HSK1"], example_count=200)
    create_deck(data, 1351853567, "HSK2", character_list=HSK["HSK2"], example_count=200)
    create_deck(data, 1338145300, "HSK3", character_list=HSK["HSK3"], example_count=200)
    create_deck(data, 1514431534, "HSK4", character_list=HSK["HSK4"], example_count=200)
    create_deck(data, 1619351713, "HSK5", character_list=HSK["HSK5"], example_count=200)
    create_deck(data, 1125780287, "HSK6", character_list=HSK["HSK6"], example_count=200)


if __name__ == '__main__':
    main()
