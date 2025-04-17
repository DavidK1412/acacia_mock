from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
from typing import List, Dict, Union
import random
import uuid

app = FastAPI()

# Simulador en memoria
games_db: Dict[str, Dict] = {}

# ----- MODELOS -----

class GameCreateRequest(BaseModel):
    game_id: str  # ya no validamos UUID

class MovementRequest(BaseModel):
    movement: List[int]

class BaseResponse(BaseModel):
    type: str
    actions: Dict

# ----- RESPUESTAS POSIBLES -----

def generate_random_text() -> str:
    options = [
        "Buen trabajo.",
        "Vamos bien, sigue así.",
        "¿Probamos algo diferente?",
        "¡Eso fue interesante!",
        "Analizando movimiento..."
    ]
    return random.choice(options)

def generate_random_video() -> str:
    return f"VIDEO{random.randint(1, 5)}.MP4"

def generate_random_state() -> List[int]:
    """
    Genera un estado aleatorio con los números del 0 al 6 sin repetir.
    """
    state = list(range(7))  # Contiene 0 a 6
    random.shuffle(state)
    return state


# ----- ENDPOINTS -----

@app.post("/game")
def create_game(game: GameCreateRequest):
    game_id = game.game_id
    games_db[game_id] = {
        "movements": [],
        "difficulty": 1
    }
    return {"message": "Game created", "game_id": game_id}


@app.post("/game/{game_id}")
def update_game(game_id: str, data: MovementRequest):
    if game_id not in games_db:
        games_db[game_id] = {"movements": [], "difficulty": 1}

    games_db[game_id]["movements"].append(data.movement)

    response_type = random.choice(["SPEECH", "CHANGE_DIFF", "TUTORIAL", "CORRECT", "ASK"])

    if response_type == "SPEECH":
        return {
            "type": "SPEECH",
            "actions": {
                "text": generate_random_text()
            }
        }

    elif response_type == "CHANGE_DIFF":
        level_change = random.choice([-1, 1])
        games_db[game_id]["difficulty"] += level_change
        return {
            "type": "CHANGE_DIFF",
            "actions": {
                "text": "Ajustando dificultad...",
                "level_plus": level_change
            }
        }

    elif response_type == "TUTORIAL":
        return {
            "type": "TUTORIAL",
            "actions": {
                "text": "Te recomiendo ver este tutorial.",
                "video": generate_random_video()
            }
        }

    elif response_type == "CORRECT":
        last_state = generate_random_state()
        best_next_state = generate_random_state()
        return {
            "type": "CORRECT",
            "actions": {
                "text": "Este sería un mejor movimiento.",
                "last_state": last_state,
                "best_next_state": best_next_state
            }
        }

    elif response_type == "ASK":
        return {
            "type": "ASK",
            "actions": {
                "text": "¿Quieres que te ayude con el siguiente movimiento?"
            }
        }


@app.get("/game/{game_id}/best_next")
def get_best_next(game_id: str):
    if game_id not in games_db:
        games_db[game_id] = {"movements": [], "difficulty": 1}

    last_state = generate_random_state()
    best_next = generate_random_state()

    return {
        "type": "BEST_NEXT",
        "actions": {
            "text": "Este es el mejor siguiente movimiento.",
            "best_next": best_next
        }
    }
