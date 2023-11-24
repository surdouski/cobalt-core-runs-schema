Here I go making schemas again, oh boy...

This is not a shiny packaged item, you'll need to clone this and follow some simple instructions. These
instructions don't tell you how to set use venv because I'm lazy, but you should always do so when using python.

Note: Also, I was using python3.11 because I'm currently on my windows machine and idc enough to update it on this.

- Clone the repo.
- Copy your zipped jsons into a local relative directory, `runs`.
- Unzip your jsons.
- Run the following:

```bash
python3.11 -m pip install sqlalchemy
python3.11 add_rows_db.py
```

After that runs, you can then enter interactive python environment and do things by importing cc_session.

```python
# python3.11

>> from cc_session import *
runs_with_isaac = (
    session.query(CCRun)
    .join(CCCharacterLinkedRun)
    .join(CCCharacter)
    .filter(CCCharacter.name == 'goat')  # this is isaac's name in the decks
    .all()
)

# do analysis of the results or some shit
```

I might put more effort into this later if someone makes a reasonable request.
