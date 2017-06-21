import genanki

MODEL_ID = 1637360957
MODEL_NAME = 'Handwritten Character'

QUESTION = "What character is this?<br>"
ANSWER = "{{FrontSide}}<hr id=\"answer\">{{type:Character}}"

card_fields = [{"name": "Character"}]
card_templates = []
for number in range(1, 31):
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


def main():
    # Print out auto-generated code for sanity check
    print("Fields")
    for field in card_fields:
        print(field)

    print("\nTemplates")
    for template in card_templates:
        print(template)


if __name__ == '__main__':
    main()
