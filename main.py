from collections import defaultdict

import genanki

from casia import CASIA
from hsk import HSK
from models import character_model


def create_deck(data, deck_id, name, character_list=None):
    # Create deck
    deck = genanki.Deck(deck_id, name)

    # Get data and create media
    deck_data = defaultdict(list)
    media = []
    for image, character in data.load_all():
        if character_list is None or character in character_list:
            filename = "%s_%s.jpg" % (character, len(deck_data[character]))
            print(filename)
            #image.save(filename)
            deck_data[character].append(filename)
            media.append(filename)

    # Create notes
    for character in deck_data:
        note_fields = [character]
        examples = ["<img src=\"%s\">" % image for image in data[character]]
        note_fields.extend(examples)
        print(note_fields)
        #my_note = genanki.Note(model=character_model, fields=note_fields)
        # deck.add_note(my_note)

    # Create the package and output
    #package = genanki.Package(deck)
    #package.media_files = media
    #package.write_to_file('%s.apkg' % name)



def main():
    data = CASIA()
    create_deck(data, 2041831503, "HSK1", character_list=HSK["HSK1"])


if __name__ == '__main__':
    main()
