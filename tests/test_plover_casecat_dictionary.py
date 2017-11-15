"""Unit tests for CaseCat."""

import os
import unittest

from plover_casecat_dictionary import CaseCatDictionary

class CaseCatDictionaryTestCase(unittest.TestCase):

    def test_load_dictionary(self):

        for filename, expected in (

                (u'S-abc.sgdct',
                    {('S',): u'abc'}),
                (u'S-abc,T-abc.sgdct',
                    {('S',): u'abc', ('T',): u'abc'}),
                (u'S-dis.sgdct',
                    {('S',): u'{dis^}'}),
                (u'S-ing.sgdct',
                    {('S',): u'{^ing}'}),
                (u'S_S-abc.sgdct',
                    {('S','S'): u'abc'}),

                # No test for "cap up", because
                # we don't yet have a genuine file
                # that contains it

                ):

            d = CaseCatDictionary.load(os.path.join('tests', filename))
            self.assertEqual(dict(d.items()), expected)
