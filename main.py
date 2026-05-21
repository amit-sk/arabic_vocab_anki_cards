import requests
import json


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
        "modelName": "Basic (and reversed card)",
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": ["api"]
    }
    return invoke("addNote", note=note)


def add_audio_flashcard(audio_url, back, front=None):
    note = {
        "deckName": DECK_NAME,
        "modelName": "Basic",
        "fields": {
            "Front": front if front is not None else "audio",
            "Back": back
        },
        "tags": ["api", "audio"],
        "audio": {
            "url": audio_url,
            "filename": audio_url.split('/')[-1],
            "fields": ["Front"]
        }
    }
    return invoke("addNote", note=note)


def words_intro():
    with open('words_intro.txt', 'r', encoding="utf-8") as f:
        words = f.read().splitlines()
        for word in words:
            front = word[:word.find('(')]
            back = word[word.find('(') + 1 : word.find(')')]
            add_flashcard(front=front, back=back)

def words_lesson_i(i):
    with open(f'words_lesson{i}.txt', 'r', encoding="utf-8") as f:
        words = f.read().splitlines()
        for word in words:
            front = word[:word.find('|')]
            back = word[word.find('|') + 1:]
            add_flashcard(front=front, back=back)

def audio_lesson_i(i):
    with open(f'audio_lesson{i}.json', 'r', encoding="utf-8") as f:
        words = json.load(f)
        for front, back in words.items():
            add_audio_flashcard(audio_url=front, back=back)

def main():
    # test connection
    print("AnkiConnect version:", invoke("version"))
    # invoke("createDeck", deck=DECK_NAME)
    # words_intro()
    # words_lesson(i=1)
    # audio_lesson(i=1)
    words_lesson_i(i=2)
    audio_lesson_i(i=2)


if __name__ == "__main__":
    main()
