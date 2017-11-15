import re
from struct import unpack
from plover.steno_dictionary import StenoDictionary

KEYS = 'STKPWHRAO*EUFRPBLGTSDZ'

# I admit this is a wild guess
ENCODING = 'latin-1'


class CaseCatDictionary(StenoDictionary):

    @staticmethod
    def _tidy_translation(translation):

        result = translation.decode(ENCODING)

        curly_brackets = False

        # these codes have been figured out
        # by inspecting saved dictionaries;
        # they may be wrong.

        if result.startswith('\x10\x81'):
            # prefix
            result = f'^{result}'
            curly_brackets = True

        if result.endswith('\x10\x01'):
            # suffix
            result = f'{result}^'
            curly_brackets = True

        if curly_brackets:
            result = '{' + result + '}'

        if '\x0E' in result:
            # cap up
            result += '{-|}'

        result = re.sub(r'[^ -~]', '', result)
        return result

    def _parse(self, filename):
        with open(filename, 'rb') as f:

            f.seek(0x280)

            while True:

                unknown1 = f.read(18)
                if unknown1 is None or len(unknown1) != 18:
                    return

                stroke_count = unpack(">B", f.read(1))[0]
                letter_count = unpack(">B", f.read(1))[0]

                f.read(1)

                strokes = []

                for _ in range(stroke_count):
                    stroke = ''
                    stroke_bits = unpack(">L", f.read(4))[0]

                    for k, steno_key in enumerate(KEYS):
                        bit = 0x80000000 >> k
                        if steno_key == '*' and stroke == '':
                            stroke += '-'

                        if stroke_bits & bit:
                            stroke += steno_key
                    strokes.append(stroke)

                translation = self._tidy_translation(f.read(letter_count))

                yield (tuple(strokes), translation)

                padding_space = f.tell() % 4

                if padding_space != 0:
                    f.read(4 - padding_space)

    def _load(self, filename):
        self.update(self._parse(filename))
        self.readonly = True
