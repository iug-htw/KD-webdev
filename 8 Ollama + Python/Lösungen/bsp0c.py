import json

def main():
    # 1. Python-Datenstruktur (Dictionary mit Liste)
    person = {
        "name": "Anna",
        "age": 11,
        "hobbies": ["Lesen", "Minecraft", "Schwimmen"],
        "program": ["KD" ]
    }

    print("Python-Objekt Person:")
    print(person)

    # 2. In JSON-Text umwandeln (serialisieren)
    person_json = json.dumps(person, indent=2)
    print("\nPython-Objekt als JSON-Text:")
    print(person_json)

    # 3. JSON-Text zurück in Python-Objekt (deserialisieren)
    person_back = json.loads(person_json)
    print("\nZurück in Python umgewandelt:")
    print(person_back)




if __name__ == "__main__":
    main()
