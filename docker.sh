#!/bin/sh


function build_image() {
    docker build -t spichki-game/game-scene:mvp . --no-cache
}


function create_container() {
    docker create \
	   --interactive \
	   --tty \
	   --name game-scene \
	   --hostname game-scene \
	   --ip 172.30.100.101 \
	   --publish 50000:50051 \
	   spichki-game/game-scene:mvp

    # docker export 7423d238b | docker import — sample:flat
}


function help() {
    echo ""
    echo " Available parameters:"
    echo ""
    echo "    --build-image"
    echo "    --create-container"
    echo "    --help"
    echo ""
}


if [ -n "$1" ]
then
   case "$1" in
       --build-image) build_image;;
       --create-container) create_container;;
       --help) help;;
       *) echo "[ ERROR ]: Unknown parameter '${1}', use --help";;
   esac
else
    echo "[ ERROR ]: Expected parameter, use --help"
fi
