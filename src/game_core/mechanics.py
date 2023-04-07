from secrets import SystemRandom
from itertools import cycle

from .models import SetMatches, Player


class GameMatch:
    RNG: 'SystemRandom' = SystemRandom()

    def __init__(self):
        self.__matches: 'SetMatches' = SetMatches()
        self.__players: list['Player'] = []
        self.__outsiders: list['Player'] = []
        self.__move: 'Player' | None = None
        self.__winner: 'Player' | None = None
        self.__cycle_players: cycle | None = None

    def __set_random_num_matches(self) -> None:
        num_min = len(self.__players) * 10
        num_max = num_min + 15
        random_num = self.RNG.randint(num_min, num_max)

        self.__matches.number = random_num

    def __random_shuffle_players(self) -> None:
        self.RNG.shuffle(self.__players)

    def __set_next_move(self) -> None:
        self.__move = next(self.__cycle_players)

        for _ in self.__players:
            next_move = next(self.__cycle_players)
            if next_move in self.__outsiders:
                continue
            else:
                self.__move = next_move
                break

    @property
    def matches(self) -> int | None:
        return self.__matches.number

    @property
    def players(self) -> list[str]:
        return [player.name for player in self.__players]

    @property
    def outsiders(self) -> list[str]:
        return [outsider.name for outsider in self.__outsiders]

    @property
    def winner(self) -> str | None:
        return self.__winner.name if self.__winner else None

    @property
    def move(self) -> str | None:
        return self.__move.name if self.__move else None

    def add_players(self, *names: str) -> None:
        if self.__winner:
            raise RuntimeError(
                "You cannot add players after finish"
            )

        if self.__move:
            raise RuntimeError(
                "You cannot add players during the game"
            )

        if len(names) != len(set(names)):
            raise RuntimeError(
                "Non-unique player names"
            )

        if len(names) + len(self.__players) > 10:
            raise RuntimeError(
                "No more than 10 players are allowed"
            )

        for name in names:
            self.__players.append(
                Player(name, self.__matches)
            )

    def start(self) -> None:
        if self.__winner:
            raise RuntimeError(
                "You cannot start the same game after finish"
            )

        if self.__move:
            raise RuntimeError(
                "You cannot restart during the game"
            )

        if len(self.__players) < 2:
            raise RuntimeError(
                "At least 2 players are needed for start the game"
            )

        self.__set_random_num_matches()
        self.__random_shuffle_players()

        self.__cycle_players = cycle(self.__players)
        self.__set_next_move()

    def make_move(self, num_matches: int) -> None:
        if not self.__move:
            raise RuntimeError(
                "The player is allowed to make move only during the game"
            )

        if not 1 <= num_matches <= 3:
            raise RuntimeError(
                "The player is allowed to take from 1 to 3 matches"
            )

        self.__move.take_matches(num_matches)
        self.__set_next_move() if self.__matches.number else self.stop()

    def stop(self, player_name: str | None = None) -> None:
        if self.__winner:
            raise RuntimeError(
                "You cannot stop the game when the game is already stopped"
            )

        if self.__matches.number == 0:
            self.__winner = self.__move
            self.__move = None

        elif player_name:
            if len(self.__players) > 2:
                self.__outsiders.append(
                    self.__players[
                        self.__players.index(player_name)
                    ]
                )

                if player_name == self.__move:
                    self.__set_next_move()

            else:
                if player_name == self.__move:
                    self.__set_next_move()

                self.__winner = self.__move

        else:
            raise RuntimeError(
                "You cannot stop the game for all players now"
            )
