# Treffen
This project aims to implement a Killer game (also known as The Game of Assassination), but expand it with multiple modes.

## The game in brief
The core principle is the following: every player involved in a game receive a *ziel* (german word for target) and a *mission*. In our example, if Alice and Bob are players, Bob will be the *ziel* of Alice and her *mission* will be *Dance with your ziel at least during one song*. If Alice succeeds, she will announce it to Bob, which discovers who was his "hunter" (*jaeger* in the game), and give her his player code. Alice will now receive a new *ziel* and a new mission, and Bob will be out. The game continue until there is a single player.

## Implementation
The game is developed in the form of a web applicaition built on the Django Framework and deployed on Clever Cloud (because 🇫🇷 hosting is ❤️ ).

### Developement setup
Prerequesites : Postgresql, Python 3.9 at least, Pip. Done on Manjaro/ArchLinux, no guarantee on other OS yet ¯\_(ツ)_/¯.

- Clone the project (`git clone git@github.com:Dynnammo/treffen.git && cd treffen`)
- Install your virtual environment (in my case I use [pew](https://github.com/berdario/pew))
- Go into your virtual environment (in my case `pew new treffen && pew setproject treffen`)
- Install dependancies : `pip install -r requirements.txt`
- Make migrations : `python manage.py makemigrations`
- Run : `python manage.py runserver`
- You're done. Give yourself a *Kartoffelnsalat* to celebrate.

### Production setup
On clevercloud, you'll have to link your GitHub account or installing the Clever cloud CLI.
Treffen works with a Postgres addon + a dozen of env variables.
