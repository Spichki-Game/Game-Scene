class SetMatches:
    def __init__(self):
        self.__number: int | None = None

    @property
    def number(self) -> int | None:
        return self.__number

    @number.setter
    def number(self, new_number: int) -> None:
        assert 0 <= new_number
        self.__number = new_number


class Player:
    def __init__(self, name: str, matches: 'SetMatches'):
        self.__name = name
        self.__matches = matches

    @property
    def name(self) -> str:
        return self.__name

    def take_matches(self, num: int) -> None:
        self.__matches.number -= num
