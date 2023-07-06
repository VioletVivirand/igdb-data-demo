from dotenv import load_dotenv
import os
from utils.igdb import IGDBWrapper
import asyncio
import pendulum
import pandas as pd

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if __name__ == "__main__":
    igdb = IGDBWrapper(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Get token first
    igdb.get_token()

    # Get Nintendo Switch Games released after 2022-01-01 to 2023-06-30
    query = """
    fields
      name,
      summary,
      involved_companies.publisher,
      involved_companies.company.name,
      platforms.name,
      game_modes.name,
      genres.name,
      themes.name,
      player_perspectives.name,
      first_release_date,
      url,
      artworks.url,
      screenshots.url;
    where first_release_date > 1640966400
      & first_release_date < 1688169600
      & platforms = 130;
    sort first_release_date asc;
    limit 500;
    offset 0;
    """
    games = asyncio.run(igdb.get_games(query))

    print("Finished.")

    rows = []
    for game in games:
        # No summary can affect the search performance very much,
        # so drop the game without summary
        if game.get("summary"):
            # Column "idgb_id"
            igdb_id = game["id"]
            # Column "name"
            name = game["name"]
            # Column "summary"
            summary = game["summary"]
            # Column "description"
            description_title = f'Title: "{game["name"]}" '
            description_summary = f'Summary: {game["summary"]} '
            description_release = f'Released on {pendulum.from_timestamp(game["first_release_date"]).to_formatted_date_string()}. '
            description_publishers = "Publishers: " + ", ".join([game["company"]["name"] for game in list(filter(lambda x: x["publisher"] == True, game["involved_companies"]))]) + ". " if game.get("involved_companies") else "Publishers: unknown. "
            description_platforms = "Platforms: " + ", ".join([platform["name"] for platform in game["platforms"]]) + ". "
            description_game_modes = "Game Modes: " + ", ".join([game_mode["name"] for game_mode in game["game_modes"]]) + ". " if game.get("game_modes") else "Game Modes: unknown. "
            description_genres = "Genres: " + ", ".join([genre["name"] for genre in game["genres"]]) + ". " if game.get("genres") else "Genres: unknown. "
            description_themes = "Themes: " + ", ".join([theme["name"] for theme in game["themes"]]) + ". " if game.get("themes") else "Themes: unknown. "
            description_player_perspectives = "Player Perspectives: " + ", ".join([player_perspective["name"] for player_perspective in game["player_perspectives"]]) + ". " if game.get("player_perspectives") else "Player Perspectives: unknown. "
            description = f'{description_title}{description_summary}{description_release}{description_publishers}{description_platforms}{description_game_modes}{description_genres}{description_themes}{description_player_perspectives}'.strip()
            # Column "url"
            url = game["url"]
            # Column "artwork_url_id"
            artwork_hash = game["artworks"][0]["url"].split("/")[-1].replace(".jpg", "") if game.get("artworks") else None
            # Column "screenshot_url_id"
            screenshot_hash = game["screenshots"][0]["url"].split("/")[-1].replace(".jpg", "") if game.get("screenshots") else None

            rows.append([igdb_id, name, summary, description, url, artwork_hash, screenshot_hash])
    
    df = pd.DataFrame(rows, columns=["igdb_id", "name", "summary", "description", "url", "artwork_hash", "screenshot_hash"])
    df.to_csv("nintendo_switch_games.csv", index=False)
