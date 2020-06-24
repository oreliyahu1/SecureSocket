def az_to_index(char: chr) -> int:
    valid_character(char, True)
    return ord(char.upper()) - ord('A')


def valid_character(char: chr, raise_exception: bool = False) -> bool:
    valid_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if char is None or not char.upper() in valid_chars:
        if not raise_exception:
            return False
        raise ValueError('EnigmaStatic_valid_character: unexpected character, enigma only supports A-Z characters')
    return True


def index_to_az(index: int) -> chr:
    if not 0 <= index <= 26:
        raise ValueError('EnigmaStatic_index_to_az: unexpected index, enigma only supports 0-25 index\'s')
    return chr(ord('A') + index)
