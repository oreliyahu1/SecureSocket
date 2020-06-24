from Crypto.Crypto.Enigma.EnigmaStatic import valid_character


class PlugBoard:

    def __init__(self, stecker_pairs: list = None):
        self.used_characters = []
        self.plug_board_setting = {}
        if stecker_pairs is None:
            return

        for pair in stecker_pairs:
            pair = pair.upper()
            if len(pair) != 2:
                raise ValueError('Plugboard__init__: pairs length must be 2')
            (i, j) = (pair[0], pair[1])
            valid_character(i, True)
            valid_character(j, True)
            if (i in self.used_characters) or (j in self.used_characters):
                raise ValueError('Plugboard__init__: dual uses of characters')
            else:
                self.plug_board_setting.update({i: j})
                self.plug_board_setting.update({j: i})
                self.used_characters += [i, j]

    def get_plug_char(self, char: chr) -> chr:
        if char.upper() in self.plug_board_setting:
            return self.plug_board_setting[char]
        else:
            return char
