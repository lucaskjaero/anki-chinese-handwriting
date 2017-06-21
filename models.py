import genanki

# Model ID must be unique. Randomly generated.
MODEL_ID = 1637360957
MODEL_NAME = 'Handwritten Character'

# Styling for cards.
QUESTION = "What character is this?<br>"
ANSWER = "{{FrontSide}}<hr id=\"answer\">{{type:Character}}"


def get_model(example_count=30):
    """
    Generates an anki card model for a given number of examples. 
    Allows you to get as many as you need without overloading your anki installation.
    :param example_count: The number of examples to use
    :return: A genanki.Model object
    """
    card_fields = [{"name": "Character"}]
    card_templates = []
    for number in range(1, example_count+1):
        # Create fields
        field_name = "Example %s" % number
        card_fields.append({
            "name": field_name,
        })

        card_name = "Card %s" % number
        question = "%s{{%s}}" % (QUESTION, field_name)
        card_templates.append({
            "name": card_name,
            "qfmt": question,
            "afmt": ANSWER,
        })

    character_model = genanki.Model(MODEL_ID, MODEL_NAME, fields=card_fields, templates=card_templates)

    return character_model
