# TorCrawler

> a tor network crawler
---

A Tor Network crawler writen in python that will normalize 
data and store it in a SQL database.

## Introduction
I started this project in my cybersecurity course. It was initially just a way of learning how to 
automate scrapping the web, and ended up as crawler that scrapes the Tor 
Network for new `.onion` urls. Thus creating a database full of Tor Network 
websites making it easier for me to search the network. There was also other 
ideas that we had for exploring this database, you could automate certain 
processes so that you can find specific information that you want in the 
Tor Network.

Also there can be other applications for this project that are still open for 
exploration.

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/)

## Instalation
[//]: # (In the future I should have an installation from local and one where I just use the images in the Dockerhub repo.)
```
git clone https://github.com/FilipeS0usa/TorCrawler.git
cd torcrawler
docker compose up -d
```

## Usage Examples
After setting up the project you can use the data on the database as you wish
(Ex.: Browser, Scripting for specific information,etc...)

## Development Setup (Devcontainer)

1. Install docker (check [documentation](https://docs.docker.com/engine/install/))
1. Open project in VSCode
1. Install the [Devcontainer extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
1. `ctrl + shift + p` and select `Dev Containers: Rebuild Container`
   - If container is already build select `Dev Containers: Reopen in Container`


## Decision Making
I will be storing all of my decision making in [here](docs/decision-making).
