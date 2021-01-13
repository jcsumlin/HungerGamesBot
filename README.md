# Local Development
- Unix based operating system is recommended
- Docker is not required but recommended.

0) Ensure you have at least python 3.6 installed
1) Start a postgres SQL server either with docker or other means.
2) Place connection credentials in `config.py`
3) Run the `./utils/database.py` file to create the tables.
4) Register test bot with [discord here](https://discord.com/developers/applications)
5) Place keys in `config.py`
6) Run `main.py` 


# MVP
- Create new custom hunger game
    - Game master can set custom name.
    - Game master can enable/disable items
    - Game master can enable/disable alliances
- Tributes can be nominated/renominated by users
- Items should maintain continuity (if a tribute has a weapon they will have a much larger change of killing another tribute)
    - Medicine can be used to heal tributes of natural injuries (sprained ankles, fevers, dehydration, heat stroke etv.)
- Random natural disasters can occur.
- Tributes can either go for a cornucopia or run away
- Only one winner can be survive
- Tributes can have custom names/images
- Alliances between tributes can shift. 
    - The tribute that is left is either abandoned by the previous tribute or killed in a backstabbing event
    - Items are shared in alliances 
