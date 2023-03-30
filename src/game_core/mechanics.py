from secrets import SystemRandom
from itertools import cycle

from game_core.models import SetMatches, Player


class GameMatch:
    RNG: 'SystemRandom' = SystemRandom('game')

    def __init__(self):
        self.__matches: 'SetMatches' = SetMatches()
        self.__players: list['Player'] = []
        self.__outsiders: list['Player'] = []
        self.__move: 'Player' | None = None
        self.__winner: 'Player' | None = None

    def __set_random_num_matches(self) -> None:
        num_min = len(self.__players) * 10
        num_max = num_min + 15
        random_num = self.RNG.randint(num_min, num_max)

        self.__matches.number = random_num

    def __random_shuffle_players(self) -> None:
        self.RNG.shuffle(self.__players)

    def __set_next_move(self) -> None:
        if not self.__set_next_move.__dict__:
            self.__set_next_move.__dict__.update(
                players=cycle(self.__players)
            )

        for _ in self.__players:
            next_move = next(self.__set_next_move.players)
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
        return [self.__outsiders.name for outsider in self.__outsiders]

    @property
    def winner(self) -> str | None:
        return self.__winner.name if self.__winner else None

    @property
    def move(self) -> str | None:
        return self.__move.name if self.__move else None

    def add_players(self, *names: str) -> None:
        assert not self.__winner
        assert not self.__move
        assert len(names) == len(set(names))

        for name in names:
            self.__players.append(
                Player(name, self.__matches)
            )

    def start(self) -> None:
        assert not self.__winner
        assert not self.__move
        assert len(self.__players) > 2

        self.__set_random_num_matches()
        self.__random_shuffle_players()
        self.__set_next_move()

    def make_move(self, num_matches: int) -> None:
        assert self.__move
        assert 1 <= num_matches <= 3

        self.__move.take_matches(num_matches)
        self.__set_next_move() if self.__matches.number else self.stop()

    def stop(self) -> None:
        assert not self.__winner

        if self.__matches.number == 0:
            self.__winner = self.__move
        elif len(self.__players) > 2:
            self.__outsiders.append(self.__move)
            self.__set_next_move()
        else:
            self.__set_next_move()
            self.__winner = self.__move

        self.__move = None