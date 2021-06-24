from plover.steno_dictionary import StenoDictionary
from plover.steno import normalize_steno
from struct import unpack
import re


KEYS = '#STKPWHRAO*EUFRPBLGTSDZ'
RIGHT_KEYS_INDEX = KEYS.index('E')

# I admit this is a wild guess
ENCODING = 'latin-1'

def _tidy_translation(t):

    result = t.decode(ENCODING)

    curly_brackets = False

    # these codes have been figured out
    # by inspecting saved dictionaries;
    # they may be wrong.

    if result.startswith('\x10\x81'):
        # prefix
        result = '^' + result
        curly_brackets = True

    if result.endswith('\x10\x01'):
        # suffix
        result = result + '^'
        curly_brackets = True

    if '\x0E' in result:
        # cap up
        result += '{-|}'

    if curly_brackets:
        result = '{' + result + '}'

    result = re.sub(r'[^ -~]', '', result)
    return result


def _load_dictionary(f):

    f.seek(0x280)

    while True:

        unknown1 = f.read(18)
        if unknown1 is None or len(unknown1) != 18:
            return

        stroke_count = unpack(">B", f.read(1))[0]
        letter_count = unpack(">B", f.read(1))[0]

        unknown2 = f.read(1)

        steno = ''

        for i in range(stroke_count):
            if steno:
                steno += '/'

            stroke_bits = unpack(">L", f.read(4))[0]

            for n, k in enumerate(KEYS):
                if stroke_bits & (0x100000000 >> n):
                    if n >= RIGHT_KEYS_INDEX and not steno or steno.endswith('/'):
                        steno += '-'
                    steno += k

        translation = _tidy_translation(f.read(letter_count))

        yield normalize_steno(steno), translation

        padding_space = f.tell()%4
        if padding_space != 0:
            f.read(4 - padding_space)


class CaseCatDictionary(StenoDictionary):

    readonly = True

    def _load(self, filename):
        with open(filename, 'rb') as f:
            self.update(_load_dictionary(f))
