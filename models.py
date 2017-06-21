import genanki

MODEL_ID = 1637360957
MODEL_NAME = 'Handwritten Character'

QUESTION = "What character is this?<br>"
ANSWER = "{{FrontSide}}<hr id=\"answer\">{{type:Character}}"


def get_model(example_count=30, debug=False):
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

    if debug:
        print("Fields")
        for field in card_fields:
            print(field)

        print("\nTemplates")
        for template in card_templates:
            print(template)

    return character_model

def main():
    # Print out auto-generated code for sanity check
    get_model(example_count=10, debug=True)


if __name__ == '__main__':
    main()
