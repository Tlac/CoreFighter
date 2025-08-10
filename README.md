# CoreFighter

Deck builder and stats view for Gundam TCG game

### Running it locally

```
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

### To-do list

#### Frontend

- [ ] Add home page (A little blurb about what the site is, featured decks)
    - [ ] Add nav bar
        - [ ] Add login button
        - [ ] Add Profile button
        - [ ] Add logout button
    - [ ] Add public deck list page
- [x] Add create account and login page
- [ ] Add decklist creator page
- [ ] Add stats page
    - [ ] Add bar chart showing spread of card cost
    - [ ] Add bar chart showing spread of card levels
    - [ ] Add pie chart showing amount of cards in each colour
    - [ ] Add pie chart showing amount of different card types (Unit, Pilot, Command/Pilot, Command)
    - [ ] Brainstorm section to show cards that can link
        - [ ] Add section
- [ ] Add profile page
    - [ ] Add Deck list page
    - [ ] Add username change logic
    - [ ] Add user profile image section

#### Backend

- [x] Add Gundam Card Model
- [x] Add DeckList Model
- [x] Add GET/POST/UPDATE/DELETE decklist endpoint
    - [x] Add the appropriate serializers and views
    - [ ] Add tests
- [ ] Add user profile image url to user table

#### Other

- [ ] Add CI/CD (Probably Github with Vercel integration)
- [ ] Set bucket in AWS for storing images