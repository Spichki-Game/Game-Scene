from functools import wraps
from typing import Callable, Any

from grpc_api import game_scene_pb2 as msg
from game_scene.accessor import read_session

import typing

if typing.TYPE_CHECKING:
    import grpc
    from game_core import GameMatch


def check_session_exists(method: Callable) -> Callable:
    @wraps(method)
    async def wrapper(

            self,
            request: msg.Players,
            context: 'grpc.aio.ServicerContext'

    ) -> tuple[str, 'GameMatch']:

        game = read_session(request.session_id)

        if game:
            game.start()
        else:
            return await method(self, request, context)

    return wrapper


def check_winner_game(method: Callable) -> Callable:
    @wraps(method)
    async def wrapper(

            self,
            request: msg.Game,
            context: 'grpc.aio.ServicerContext'

    ) -> tuple[str, 'GameMatch']:

        game = read_session(request.session_id)

        if game.winner:
            return await method(self, request, context)
        else:
            game.stop()

    return wrapper


def format_return(selective_state: bool = False,
                  end_response: bool = False) -> Callable:

    def decorator(method: Callable) -> Callable:
        @wraps(method)
        async def wrapper(

                self,
                request: Any,
                context: 'grpc.aio.ServicerContext'

        ) -> msg.Response:

            try:
                game = await method(self, request, context)

            except Exception as err:
                return msg.Response(
                    confirm_status=False,
                    error_body=msg.ResponseError(
                        error_type=err.__class__.__name__
                        error_msg=err.__str__()
                    )
                )

            if end_response:
                return msg.Response(
                    confirm_status=True
                )

            elif selective_state:
                game_state = {}

                for code in request.codes:
                    match code:
                        case msg.STATE_ALL:
                            game_state.update(
                                matches=game.matches,
                                move=game.move,
                                winner=game.winner,
                                players=game.players,
                                outsiders=game.outsiders
                            )

                        case msg.STATE_MATCHES:
                            game_state.update(
                                matches=game.matches
                            )

                        case msg.STATE_MOVE:
                            game_state.update(
                                move=game.move
                            )

                        case msg.STATE_WINNER:
                            game_state.update(
                                winner=game.winner
                            )

                        case msg.STATE_PLAYERS:
                            game_state.update(
                                players=game.players
                            )

                        case msg.STATE_OUTSIDERS:
                            game_state.update(
                                outsiders=game.outsiders
                            )

            else:

                game_state = {
                    'matches': game.matches,
                    'move': game.move,
                    'winner': game.winner,
                    'players': game.players,
                    'outsiders': game.outsiders
                }

            return msg.Response(
                confirm_status=True,
                state_body=msg.ResponseState(
                    **game_state
                )
            )

        return wrapper
    return decorator
