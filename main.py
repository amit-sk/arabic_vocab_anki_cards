import requests


DECK_NAME = 'arabic vocab'


def invoke(action, **params):
    r = requests.post("http://localhost:8765", json={
        "action": action,
        "version": 6,
        "params": params
    })
    r.raise_for_status()
    data = r.json()
    if data.get("error") is not None:
        if 'cannot create note because it is a duplicate' == data["error"]:
            pass
        else:
            raise RuntimeError(data["error"])
    return data["result"]


def add_flashcard(front, back):
    note = {
        "deckName": DECK_NAME,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": ["api"]
    }
    return invoke("addNote", note=note)


def words_intro():
    with open('words_intro.txt', 'r', encoding="utf-8") as f:
        words = f.read().splitlines()
        for word in words:
            front = word[:word.find('(')]
            back = word[word.find('(') + 1 : word.find(')')]
            add_flashcard(front=front, back=back)


def main():
    # test connection
    print("AnkiConnect version:", invoke("version"))


if __name__ == "__main__":
    main()
