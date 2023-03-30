"""
This package provide a public API
for the domain part of the matches game.


Class: GameAPI

[ attrs ]:

+ players: list[str]
+ outsiders: list[str]
+ matches: None | int
+ move: None | str
+ winner: None | str


[ methods ]:

+ add_players(*names: str) -> None
+ make_move(num_matches: int) -> None
+ start() -> None
+ stop() -> None

"""

from game_core.mechanics import GameMatch


__all__ = ['GameMatch']
