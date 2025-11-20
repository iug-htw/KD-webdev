import json

def main():
    # 1. Python-Datenstruktur (Dictionary mit Liste)
    people = [
        {
            "name": "Anna",
            "age": 21,
            "hobbies": ["Lesen", "Minecraft"],
            "program": ["KD" ]
        },
        {
            "name": "Ben",
            "age": 22,
            "hobbies": ["Fußball", "Programmieren"],
            "program": ["KD" ]
        }
    ]

    print("Python-Objekt People:")
    print(people)

    # 2. In JSON-Text umwandeln (serialisieren)
    people_json = json.dumps(people, indent=2)
    print("\nPython-Objekt als JSON-Text:")
    print(people_json)

    # 3. JSON-Text zurück in Python-Objekt (deserialisieren)
    people_back = json.loads(people_json)
    print("\nZurück in Python umgewandelt:")
    print(people_back)

    #eine bestimmte Person auslesen
    person2 = people_back[1]
    print("\nPerson 2:")
    print(person2)

if __name__ == "__main__":
    main()
