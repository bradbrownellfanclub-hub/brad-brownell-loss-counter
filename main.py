
import os
import json
import requests
import tweepy
from pathlib import Path
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont, ImageOps

# ---------------- CONFIGURATION ----------------

STARTING_LOSSES = 207
STATE_FILE = Path("state.json")
PHOTO_FILE = Path("assets/brad.jpg")
OUTPUT_FILE = Path("post.png")

ESPN_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/"
    "basketball/mens-college-basketball/scoreboard"
)

# ---------------- STATE ----------------

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())

    return {
        "losses": STARTING_LOSSES,
        "processed_games": [],
        "initialized": False
    }


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ---------------- GAME MONITORING ----------------

def get_recent_games():
    games = {}

    # Check the last 7 days to catch delayed or missed updates.
    for offset in range(7):
        date = datetime.now(timezone.utc) - timedelta(days=offset)
        date_string = date.strftime("%Y%m%d")

        response = requests.get(
            ESPN_URL,
            params={"dates": date_string},
            timeout=20
        )
        response.raise_for_status()

        events = response.json().get("events", [])

        for event in events:
            games[event["id"]] = event

    return list(games.values())


def get_clemson_result(game):
    for competition in game.get("competitions", []):
        competitors = competition.get("competitors", [])

        clemson = next(
            (
                team for team in competitors
                if team.get("team", {}).get("displayName", "")
                == "Clemson Tigers"
            ),
            None
        )

        if not clemson:
            continue

        status = game.get("status", {}).get("type", {})

        if not status.get("completed", False):
            return None

        opponent = next(
            team for team in competitors if team != clemson
        )

        clemson_score = int(clemson["score"])
        opponent_score = int(opponent["score"])

        return {
            "loss": clemson_score < opponent_score,
            "clemson_score": clemson_score,
            "opponent_score": opponent_score,
            "opponent": opponent["team"]["displayName"]
        }

    return None


# ---------------- GRAPHIC GENERATION ----------------

def create_graphic(losses):
    if not PHOTO_FILE.exists():
        raise FileNotFoundError(
            "Add Brad Brownell's photo at assets/brad.jpg"
        )

    width, height = 1200, 675
    orange = (245, 102, 0)

    canvas = Image.new("RGB", (width, height), orange)

    photo = Image.open(PHOTO_FILE).convert("RGB")
    portrait = ImageOps.fit(photo, (590, height))
    canvas.paste(portrait, (0, 0))

    draw = ImageDraw.Draw(canvas)

    bold_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    title_font = ImageFont.truetype(bold_font, 42)
    number_font = ImageFont.truetype(bold_font, 180)
    subtitle_font = ImageFont.truetype(bold_font, 34)

    draw.text(
        (620, 65),
        "CLEMSON BASKETBALL",
        font=title_font,
        fill="white"
    )

    number = str(losses)
    bounds = draw.textbbox((0, 0), number, font=number_font)
    number_width = bounds[2] - bounds[0]

    draw.text(
        (620 + (540 - number_width) / 2, 210),
        number,
        font=number_font,
        fill="white"
    )

    draw.text(
        (645, 455),
        "CAREER LOSSES",
        font=subtitle_font,
        fill="white"
    )

    draw.text(
        (645, 505),
        "AT CLEMSON",
        font=subtitle_font,
        fill="white"
    )

    canvas.save(OUTPUT_FILE, quality=95)


# ---------------- X POSTING ----------------

def post_to_x(losses):
    api_key = os.environ["X_API_KEY"]
    api_secret = os.environ["X_API_SECRET"]
    access_token = os.environ["X_ACCESS_TOKEN"]
    access_secret = os.environ["X_ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuth1UserHandler(
        api_key,
        api_secret,
        access_token,
        access_secret
    )

    upload_api = tweepy.API(auth)
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    media = upload_api.media_upload(str(OUTPUT_FILE))

    caption = (
        "Brad Brownell has become the losingest coach "
        f"in Clemson Basketball history at {losses} losses"
    )

    client.create_tweet(
        text=caption,
        media_ids=[media.media_id]
    )

    print(f"Successfully posted loss #{losses}")


# ---------------- MAIN BOT ----------------

def main():
    state = load_state()
    games = get_recent_games()

    # First run: establish a baseline and avoid posting
    # about games that finished before the bot was activated.
    if not state["initialized"]:
        for game in games:
            if game.get("status", {}).get("type", {}).get(
                "completed", False
            ):
                state["processed_games"].append(game["id"])

        state["initialized"] = True
        save_state(state)
        print("Initial game history recorded.")
        return

    for game in games:
        game_id = game["id"]

        if game_id in state["processed_games"]:
            continue

        result = get_clemson_result(game)

        if result is None:
            continue

        # Record wins too, so the same game is never
        # reconsidered on a later run.
        if not result["loss"]:
            state["processed_games"].append(game_id)
            save_state(state)
            continue

        new_total = state["losses"] + 1

        print(
            f"Clemson loss detected: {result['clemson_score']}-"
            f"{result['opponent_score']} vs {result['opponent']}"
        )

        create_graphic(new_total)
        post_to_x(new_total)

        state["losses"] = new_total
        state["processed_games"].append(game_id)
        save_state(state)


if __name__ == "__main__":
    main()
