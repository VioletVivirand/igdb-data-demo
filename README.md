# (WIP) IGDB Data Download Example

| 🚧 [NOTE] This is still under construction! Use this at your own risk! 🚧

## Usage

```bash
python ./get_nintendo_switch_game_data.py
```

## Plan

* Pre-loaded Metadata
  * `platforms` (Platforms)
  * `game_modes` (Game Modes)
  * `genres` (Genre)
  * `themes` (Themes)
  * `player_perspectives` (Player Perspectives)
* Summary Sentences
  * `summary` (Summary)
    * Replace the "\n" by a white space
  * `collection` (Series)
  * `involved_companies` (Publisher)
    * Search every `involved_companies`'s ID, filter the `publisher` key has a value `true`

Example:

Name: The Legend of Zelda: Tears of the Kingdom. Summary: The Legend of Zelda: Tears of the Kingdom is the sequel to The Legend of Zelda: Breath of the Wild. The setting for Link’s adventure has been expanded to include the skies above the vast lands of Hyrule. Series:
The Legend of Zelda. Publishers: Nintendo. Platforms: Nintendo Switch. Game Modes: Single player. Genre: Adventure. Themes: Action, Fantasy, Open world, Science fiction. Player Perspectives: Third person.

Syntax:

`Title: "[game.name]" Summary: [game.summary]. Released on [game.first_release_date]. Publishers: [company.name]. Platforms: [platforms.name]. Game Modes: [game_modes.name]. Genre: [genres.name]. Themes: [themes.name]. Player Perspectives: [player_perspectives.name]`
