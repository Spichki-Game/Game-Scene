#!/bin/sh


service redis-server start
poetry run generate-api game_scene
poetry run server
