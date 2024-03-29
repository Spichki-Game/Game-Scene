import grpc
import asyncio

from grpc_api import game_scene_pb2_grpc as srv
from grpc_api import game_scene_pb2 as msg

from game_core import GameMatch

from .middleware import (
    format_return,
    check_session_not_exists,
    check_session_exists
)

from .accessor import (
    read_session,
    write_session,
    end_session
)


LISTEN_ADDR = '[::]:50051'


class GameScene(srv.GameSceneServicer):

    @format_return()
    @check_session_not_exists
    async def Start(self,
                    players: msg.Players,
                    context: grpc.aio.ServicerContext) -> msg.Response:

        game = GameMatch()

        game.add_players(*list(players.names))
        game.start()
        write_session(players.session_id, game)

        return game

    @format_return()
    @check_session_exists
    async def Move(self,
                   matches: msg.Matches,
                   context: grpc.aio.ServicerContext) -> msg.Response:

        game = read_session(matches.session_id)

        game.make_move(matches.number)
        write_session(matches.session_id, game)

        return game

    @format_return()
    @check_session_exists
    async def Leave(self,
                    player: msg.Player,
                    context: grpc.aio.ServicerContext) -> msg.Response:

        game = read_session(player.session_id)

        game.leave_player(player.name)
        write_session(player.session_id, game)

        return game

    @format_return(selective_state=True)
    @check_session_exists
    async def Get(self,
                  request_state: msg.RequestState,
                  context: grpc.aio.ServicerContext) -> msg.Response:

        game = read_session(request_state.session_id)
        return game

    @format_return(end_response=True)
    @check_session_exists
    async def Stop(self,
                   game: msg.Game,
                   context: grpc.aio.ServicerContext) -> msg.Response:

        end_session(game.session_id)


async def game_scene_server() -> None:
    server = grpc.aio.server()

    srv.add_GameSceneServicer_to_server(
        GameScene(),
        server
    )

    server.add_insecure_port(LISTEN_ADDR)

    await server.start()
    await server.wait_for_termination()


def start() -> None:
    print("[ start ]: Game Scene server\n")

    asyncio.run(
        game_scene_server()
    )
