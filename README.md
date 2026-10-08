# KAI Intent Classifier
This is my solution for the Kypson KAI Intent Classifier task.
The project takes a user message and identifies what the user is asking about. I used simple Python rules instead of any external AI or API.
## Files
- `classify.py` - main classifier and keyword baseline
- `tests.json` - test messages used to check the classifier
- `heldout.json` - results for the 15 messages given in the task
- `note.md` - examples where the classifier performs better than the baseline
- `requirements.txt` - project dependencies
## How it works
There are two functions in `classify.py`:
- `classify()` - checks the message and decides the most suitable intent.
- `keyword_baseline()` - uses simple keyword matching for comparison.
I also added rules for messages where more than one clue is present. For example, if the message contains a product specification but the user is actually asking for a supplier, the supplier request is given priority.
## How to run
Make sure Python 3 is installed.
Open the project folder and run:
```bash
python classify.py
