import argparse
from collections import defaultdict
from os import remove
from random import randrange

import genanki
from pycasia import CASIA

from hsk import HSK
from models import get_model

EXAMPLE_COUNT = 50


def create_deck(name, character_list=None, example_count=30):
    """
    Create a deck with the given requirements.
    :param name: The deck name
    :param character_list: A list of characters to select. If not given, all characters in the dataset will be used.
    :param example_count: How many examples per character to include. Default is 30. 
    :return: Nothing.
    """

    # Must be unique. See genanki details for more.
    deck_id = randrange(1 << 30, 1 << 31)

    print("Creating deck %s" % name)
    # Create deck
    deck = genanki.Deck(deck_id, name)

    # Initialize data collection
    data = CASIA.CASIA()
    deck_data = defaultdict(list)
    media = []

    # Get data and create media
    characters_loaded = 0
    for image, character in data.load_character_images():

        # Only include requested characters
        if character_list is None or character in character_list:
            # Only include as many examples as requested
            count = len(deck_data[character])
            if count < example_count:
                filename = "%s_%s.jpg" % (character, len(deck_data[character]) + 1)
                image.save(filename)
                deck_data[character].append(filename)
                media.append(filename)
                characters_loaded = characters_loaded + 1

            # Early stop if you have enough examples
            if character_list is None or characters_loaded >= len(character_list) * example_count:
                if len([character for character in deck_data if len(deck_data[character]) < example_count]) == 0:
                    break

    # Create notes
    print("Creating notes")
    for character in deck_data:
        note_fields = [character]
        examples = ["<img src=\"%s\">" % image for image in deck_data[character]]
        assert len(examples) == example_count, "Wrong number of examples for %s" % character
        note_fields.extend(examples)
        my_note = genanki.Note(model=get_model(example_count=example_count), fields=note_fields)
        deck.add_note(my_note)

    # Create the package and output
    print("Creating final output")
    package = genanki.Package(deck)
    package.media_files = media
    filename = '%s.apkg' % name
    package.write_to_file(filename)
    print("Created deck %s" % filename)

    # Delete all intermediate files
    print("Cleaning up")
    for path in media:
        remove(path)


def make_hsk_decks():
    create_deck("HSK1", character_list=HSK["HSK1"], example_count=EXAMPLE_COUNT)
    create_deck("HSK2", character_list=HSK["HSK2"], example_count=EXAMPLE_COUNT)
    create_deck("HSK3", character_list=HSK["HSK3"], example_count=EXAMPLE_COUNT)
    create_deck("HSK4", character_list=HSK["HSK4"], example_count=EXAMPLE_COUNT)
    create_deck("HSK5", character_list=HSK["HSK5"], example_count=EXAMPLE_COUNT)
    create_deck("HSK6", character_list=HSK["HSK6"], example_count=EXAMPLE_COUNT)


def main():
    # make_hsk_decks()
    parser = argparse.ArgumentParser(description='Create Anki decks based on characters .')
    parser.add_argument('name', nargs=1, type=str, help='What do we call the deck?')
    parser.add_argument('--count', nargs=1, type=int, help="How many examples to create", required=False)
    parser.add_argument('characters', nargs='*', type=str, help="Which characters should we use?")
    args = parser.parse_args()

    deck_name = args.name[0]
    characters = args.characters

    if args.count is not None:
        example_count = args.count[0]
        create_deck(deck_name, character_list=characters, example_count=example_count)
    else:
        create_deck(deck_name, character_list=characters)


if __name__ == '__main__':
    main()
