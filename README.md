# ScorvBot

Discord bot for the Grim Dawn server. Written using Python 3, [Discord.py](https://discordpy.readthedocs.io/en/stable/#), and [Redis](https://redis.io/docs/latest/get-started/) for storage.

## Table of Contents

- [Contributing](#contributing)
  - [Local Setup](#local-setup)
    - [Install Python](#install-python)
    - [Create a virtual Python environment](#create-a-virtual-python-environment)
    - [Install the bot's dependencies](#install-the-bots-dependencies)
    - [Environment variables](#environment-variables)
  - [Running the bot](#running-the-bot)
    - [Installing Docker \& Docker Compose](#installing-docker--docker-compose)
    - [Running the bot with Docker Compose](#running-the-bot-with-docker-compose)
  - [Notes on Redis](#notes-on-redis)

## Contributing

### Local Setup

Follow these steps to get the bot running on your machine.

#### Install Python

Download and install Python 3.12. Either download Python from the [downloads page](https://www.python.org/downloads/), or install Python using a package manager like [asdf](https://asdf-vm.com/) (any OS), [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/) (Windows), [Homebrew](https://docs.brew.sh/Homebrew-and-Python) (macOS), or your Linux distribution's package manager.

#### Create a virtual Python environment

It is highly recommended that you user a virtual environment for each project. This will keep your Python version and packages separate from project to project.

There are a few different virtual environment tools like [venv](https://docs.python.org/3/library/venv.html), [pyenv](https://github.com/pyenv/pyenv), and [Conda](https://docs.conda.io/projects/conda/en/latest/index.html). venv ships with Python 3. To create a virtual environment with venv run this command in the project root directory:

```sh
python3 -m venv .venv
```

This will create a `.venv` folder in the project root directory. To activate the virutal environment run this command:

```sh
source .venv/bin/activate
```

(Optional) Install [direnv](https://direnv.net/) to automatically activate your virtual environment when you change directories. Once direnv is installed create a `.envrc` file in the project root directory:

```sh
echo -e 'source .venv/bin/activate\n' > .envrc
```

Then run the following command to enable direnv:

```sh
direnv allow
```

Now direnv will automatically activate your virtual enviornment when you change to the project directory, and disable it when you leave.

#### Install the bot's dependencies

A `requirements.txt` file is included with all of the packages you need to use the bot. To install the dependencies run this command at the project root directory:

```sh
pip install -r requirements.txt
```

Additionally, we use [Black](https://black.readthedocs.io/en/stable/index.html) for formatting and [pre-commit](https://pre-commit.com/) to ensure that formatting is done automatically on push. Install these packages using this command:

```sh
pip install black pre-commit
```

Then activate pre-commit (only necessary on first-time install) to install the git hooks by running this command at the project root directory:

```sh
pre-commit install
```

#### Environment variables

Some environment variables are required for the bot to function:

```sh
DISCORD_TOKEN='<Discord app token>'
TEST_GUILD='<ID of your test server>'
TAG_APPROVAL_ID='<ID of the #channel where tag approval messages will go>'
ENV='dev'
```

Follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) for setting up a Discord app and getting a token.

You can either define these manually in your environment, or create a `.env` file at the project root directory. If you are running the bot without Docker Compose, then you will want to install [python-dotenv](https://github.com/theskumar/python-dotenv).

Additionally, if you are not using Docker Compose, you will need to provide the following variables for the connection to Redis:

```sh
REDIS_HOST_NAME=''
REDIS_HOST_PORT=''
```

### Running the bot

The recommended way to build and run the bot is with [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/). The included `Dockerfile` and `compose.yaml` have all the necessary configuration for building the bot and running the Redis.

#### Installing Docker & Docker Compose

For Windows and Mac you will need to install [Docker Desktop](https://www.docker.com/products/docker-desktop/). For Linux, follow [these instructions](https://docs.docker.com/desktop/setup/install/linux/).

#### Running the bot with Docker Compose

Docker Compose will handle building & running the bot, runing the Redis, and sets up the connection to the Redis. To start the bot with Compose run this command in the project root directory:

```sh
docker compose up
```

If you make changes to the source code or container configuration you will need to rebuild the images when you run compose. To do that run this command in the project root directory:

```sh
docker compose up --build
```

The Docker compose also creates a couple of volumes on your host machine. The first is the `logs/` folder. This folder will be populated with the bot's logs if `ENV='prod'`. The second is the `redis/data/` folder. This will contain all of the Redis persistence data so stored values are not lost between runs.

### Notes on Redis

By default, Redis is an in-memory data store. With the default configuration the data would be lost between runs. A configuration file is included at `redis/redis.conf` that enables both RDB and AOF persistence, and is loaded automatically when run with the included `compose.yaml`. You can read more about Redis persistence [here](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).
