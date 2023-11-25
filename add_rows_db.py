import os


def _make_clean(directory_path="."):
    """You may ask yourself, why are you using os.path? Why not Pathlib???? The answer is, I don't care enough to fix chatGPT's bad practices."""
    db_path = os.path.join(directory_path, "cc.db")

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Deleted cc.db in {directory_path}")
        except Exception as e:
            print(f"Error deleting cc.db: {e}")
    else:
        print("cc.db not found in the specified directory.")


_make_clean()  # I don't  want to deal with migrations, simple enough to do this for now


import json
from schema import *
from simple_data import characters, cards, artifacts
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def add_characters():
    for key, name in characters.items():
        new_character = CCCharacter(key=key, name=name)
        session.add(new_character)
        session.commit()


def add_cards():
    for key, name in cards.items():
        new_card = CCCard(key=key, name=name)
        session.add(new_card)
        session.commit()


def add_artifacts():
    for key, name in artifacts.items():
        new_artifact = CCArtifact(key=key, name=name)
        session.add(new_artifact)
        session.commit()


def _read_json_runs(directory="runs"):
    """Use relative path to the directory with your [unzipped] run jsons."""
    json_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                json_data.append(data)
    return json_data


def add_runs():
    for run in _read_json_runs():
        new_run = CCRun(
            version=run["version"],
            won=run["won"],
            duration=run["duration"],
            difficulty=run["difficulty"],
            timestamp=datetime.utcfromtimestamp(run["timestamp"] / 1000000000),
            runId=run["runId"],
            seed=run["seed"],
            ship=run["ship"],
            hullDamageTaken=run["hullDamageTaken"],
            combatTurns=run["combatTurns"],
        )
        session.add(new_run)
        session.commit()  # commit for the id

        for character_name in run["decks"]:
            new_character_linked_run = CCCharacterLinkedRun(
                run_id=new_run.id,
                character_id=session.get(CCCharacter, character_name).key,
            )
            session.add(new_character_linked_run)

        for card_object in run["cards"]:
            new_card_linked_run = CCCardLinkedRun(
                run_id=new_run.id,
                card_id=session.get(CCCard, card_object["type"]).key,
                upgrade=card_object["upgrade"],
            )
            session.add(new_card_linked_run)

        for artifact_name in run["artifacts"]:
            new_artifact_linked_run = CCArtifactLinkedRun(
                run_id=new_run.id,
                artifact_id=session.get(CCArtifact, artifact_name).key,
            )
            session.add(new_artifact_linked_run)

        session.commit()  # commit the rest


add_characters()
add_cards()
add_artifacts()
add_runs()


def print_characters():
    characters = session.query(CCCharacter).all()
    for character in characters:
        print(character.key, character.name)


def print_cards():
    cards = session.query(CCCard).all()
    for card in cards:
        print(card.key, card.name)


def print_artifacts():
    artifacts = session.query(CCArtifact).all()
    for artifact in artifacts:
        print(artifact.key, artifact.name)


print_characters()
print_cards()
print_artifacts()

# Remember to close the session when done
session.close()
