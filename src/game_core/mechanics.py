from secrets import SystemRandom
from .models import SetMatches, Player


class GameMatch:
    RNG: 'SystemRandom' = SystemRandom()

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
        next_index = self.__players.index(self.__move) + 1

        if next_index == len(self.__players):
            next_index = 0

        self.__move = self.__players[next_index]

    def __stop(self) -> None:
        if self.__winner:
            raise RuntimeError(
                "You cannot stop the game when the game is already stopped"
            )

        if self.__matches.number == 0 or len(self.__players) == 1:
            self.__winner = self.__move
            self.__move = None
        else:
            raise RuntimeError(
                "You cannot stop the game now"
            )

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
                "You cannot restart the game"
            )

        if len(self.__players) < 2:
            raise RuntimeError(
                "At least 2 players are needed for start the game"
            )

        self.__set_random_num_matches()
        self.__random_shuffle_players()

        self.__move = self.__players[0]

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
        self.__set_next_move() if self.__matches.number else self.__stop()

    def leave_player(self, player_name: str) -> None:
        if self.__winner:
            raise RuntimeError(
                "You cannot leave when the game is stopped"
            )

        if player_name not in self.__players:
            raise RuntimeError(
                "Invalid the player name"
            )

        if player_name == self.__move:
            self.__set_next_move()

        self.__outsiders.append(
            self.__players.pop(
                self.__players.index(player_name)
            )
        )

        if len(self.__players) == 1:
            self.__stop()
