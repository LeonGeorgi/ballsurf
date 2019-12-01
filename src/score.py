import json
import os
from typing import List, Tuple

filename = "ballsurf.json"


def load_score() -> List[Tuple[str, int]]:
    try:
        high_score = []
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                high_score = json.load(file)

        high_score = high_score[:5]

        return high_score
    except:
        return []


def is_record(score: int) -> bool:
    scores = load_score()

    if len(scores) < 5:
        return True

    for _, s in scores:
        if score > s:
            return True

    return False


def save(score: List[Tuple[str, int]]):
    score = sorted(score, key=lambda x: -x[1])
    with open(filename, 'w') as file:
        json.dump(score, file)
