# Treffen
This project aims to implement a Killer game (also known as The Game of Assassination), but expand it with multiple modes.

## The game in brief
The core principle is the following: every player involved in a game receive a *ziel* (german word for *target*) and a *mission*. In our example, if Alice and Bob are players, Alice has Bob as *ziel* and her *mission* could be *Dance with your ziel during one song*. If Alice succeeds, she will announce it to Bob, which discovers that Alice was his "hunter" (*jaeger* in the game), and give her his player code. Alice will now receive a new *ziel* and a new mission, and Bob will be out. The game continue until there is a single player left.

*How to start a game*
- On a running instance, go the admin panel: if you're instance is hosted on treffen.example.com, the URL will be treffen.example.com/admin.
- Enter your superuser credentials
- Create a Game object. Choose the name wisely: it'll be the key to enter in the game
- Create the required Missions you want for this Game. Don't forget to re-set the Game by linking missions to the game!
- You can now announce your game to all players by giving them its name !
- When everybody is registered, edit your game by switching its status from "Waiting to start" to "Started"
- You're done ! The game is now running. You can see the advancement of the game on the `/dashboard` page(only accessible to superusers).

## Implementation
The game is developed in the form of a web application built on the Django Framework and can currently by deployed through the following ways. If your's is missing please check out the infra issues [here](https://github.com/Dynnammo/treffen/issues?q=is%3Aopen+is%3Aissue+label%3Ainfra).
- Docker deployment
- Clever Cloud (because 🇫🇷 hosting is ❤️ ).

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
#### Running with CleverCloud 🇫🇷
On clevercloud, you'll have to link your GitHub account or installing the Clever cloud CLI.
Treffen works with a Postgres addon + a dozen of env variables provided in the [.env.example file](https://github.com/Dynnammo/treffen/blob/master/.env.example)

#### Running with Docker 🐋
1. Clone the project 
```
git clone git@github.com:Dynnammo/treffen.git && cd treffen
```
2. Build the image
```
docker-compose build
```
3. Up the image (this will run all the development setup process)
```
docker-compose up (-d)
```
> If you need to change any configuration such as db port, user, password, etc...,You can set it into the docker-compose.yml file
3. Re - run migrations within the container
```
docker exec -it treffen_app python manage.py migrate       
```

#### Running on Ubuntu server
Work in progress

## Contributing
See [CONTRIBUTING.md](https://github.com/Dynnammo/treffen/blob/master/CONTRIBUTING.md) file
