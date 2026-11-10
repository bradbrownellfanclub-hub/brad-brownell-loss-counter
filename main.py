
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone

STARTING_LOSSES = 207
STATE_FILE = Path("state.json")

ESPN_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/"
    "basketball/mens-college-basketball/scoreboard"
)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())

    return {
        "losses": STARTING_LOSSES,
        "processed_games": [],
        "initialized": False
    }


def save_state(state):
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2))
    temporary.replace(STATE_FILE)


def get_recent_games():
    games = {}

    for offset in range(7):
        date = datetime.now(timezone.utc) - timedelta(days=offset)

        response = requests.get(
            ESPN_URL,
            params={"dates": date.strftime("%Y%m%d")},
            timeout=20
        )
        response.raise_for_status()

        for event in response.json().get("events", []):
            games[event["id"]] = event

    return list(games.values())


def get_clemson_result(game):
    if not game.get("status", {}).get(
        "type", {}
    ).get("completed", False):
        return None

    for competition in game.get("competitions", []):
        teams = competition.get("competitors", [])

        clemson = next(
            (
                team for team in teams
                if team.get("team", {}).get("displayName")
                == "Clemson Tigers"
            ),
            None
        )

        if clemson is None:
            continue

        opponent = next(
            team for team in teams if team is not clemson
        )

        return {
            "loss": int(clemson["score"]) <
                    int(opponent["score"]),
            "opponent": opponent["team"]["displayName"],
            "clemson_score": int(clemson["score"]),
            "opponent_score": int(opponent["score"])
        }

    return None


def main():
    state = load_state()
    games = get_recent_games()

    # First run establishes the history baseline.
    if not state["initialized"]:
        for game in games:
            if game.get("status", {}).get(
                "type", {}
            ).get("completed", False):
                state["processed_games"].append(game["id"])

        state["initialized"] = True
        save_state(state)
        print("Baseline established. No posts made.")
        return

    processed = set(state["processed_games"])

    new_games = sorted(
        games,
        key=lambda game: game.get("date", "")
    )

    for game in new_games:
        game_id = game["id"]

        if game_id in processed:
            continue

        result = get_clemson_result(game)

        if result is None:
            continue

        state["processed_games"].append(game_id)
        processed.add(game_id)

        if result["loss"]:
            state["losses"] += 1

            print(
                f"CLEMSON LOSS: {result['opponent']} "
                f"{result['opponent_score']} - "
                f"Clemson {result['clemson_score']}"
            )

            print(f"Updated Brownell loss total: {state['losses']}")

            # Publishing will be connected separately.
            print("Graphic and post pending publishing setup.")

        save_state(state)


if __name__ == "__main__":
    main()
