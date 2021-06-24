"""Unit tests for CaseCat."""

from pathlib import Path

from plover_build_utils.testing import dictionary_test

from plover_casecat_dictionary import CaseCatDictionary


@dictionary_test
class TestCaseCatDictionary:

    DICT_CLASS = CaseCatDictionary
    DICT_EXTENSION = 'sgdct'
    DICT_REGISTERED = True
    DICT_LOAD_TESTS = (
        lambda: (
            'S-abc.sgdct',
            '''
            'S': 'abc',
            '''
        ),
        lambda: (
            'S-abc,T-abc.sgdct',
            '''
            'S': 'abc',
            'T': 'abc',
            '''
        ),
        lambda: (
            'S-dis.sgdct',
            '''
            'S': '{dis^}',
            '''
        ),
        lambda: (
            'S-ing.sgdct',
            '''
            'S': '{^ing}',
            '''
        ),
        # No test for "cap up", because we don't yet
        # have a genuine file that contains it.
    )
    DICT_SAMPLE = 'S-abc.sgdct'

    @staticmethod
    def make_dict(contents):
        path = Path(__file__).parent / contents
        return path.read_bytes()
