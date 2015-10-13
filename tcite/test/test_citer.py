# -*- coding: utf-8 -*-
from twisted.trial.unittest import TestCase


from tcite.citer import Citer


class CiterTest(TestCase):

    original = u'''The word duck comes from Old English *dūce "diver", a derivative of the verb *dūcan "to duck, bend down low as if to get under something, or dive", because of the way many species in the dabbling duck group feed by upending; compare with Dutch duiken and German tauchen "to dive".

This word replaced Old English ened/ænid "duck", possibly to avoid confusion with other Old English words, like ende "end" with similar forms. Other Germanic languages still have similar words for "duck", for example, Dutch eend "duck" and German Ente "duck". The word ened/ænid was inherited from Proto-Indo-European; compare: Latin anas "duck", Lithuanian ántis "duck", Ancient Greek nēssa/nētta (νῆσσα, νῆττα) "duck", and Sanskrit ātí "water bird", among others.

A duckling is a young duck in downy plumage[1] or baby duck;[2] but in the food trade young adult ducks ready for roasting are sometimes labelled "duckling".
'''
    
    point_expectations = [
        # (character after point, index, expected point citation)
        (u'T', 0, 'p0'),
        (u'h', 1, 'c1'),
        (u'e', 2, 'c2'),
        (u' ', 3, 'w1'),
        (u'w', 4, 'w1'),
        (u'o', 5, 'w1c1'),
        (u'r', 6, 'w1c2'),
        (u'd', 7, 'w1c3'),
        (u' ', 8, 'w2'),
        (u'd', 9, 'w2'),
        (u'u', 10, 'w2c1'),
        (u'c', 11, 'w2c2'),
        (u'k', 12, 'w2c3'),
        (u' ', 13, 'w3'),
        # next paragraph
        (u'\n', 280, 'p1'),
        (u'\n', 281, 'p1'),
        (u'T', 282, 'p1'),
        (u'h', 283, 'p1c1'),
        (u'i', 284, 'p1c2'),
        (u's', 285, 'p1c3'),
        (u' ', 286, 'p1w1'),
        (u'w', 287, 'p1w1'),
        (u'o', 288, 'p1w1c1'),
        (u'r', 289, 'p1w1c2'),
        (u'd', 290, 'p1w1c3'),
        (u' ', 291, 'p1w2'),
        # ...
        (u'e', 313, 'p1w5'),
        (u'n', 314, 'p1w5c1'),
        (u'e', 315, 'p1w5c2'),
        (u'd', 316, 'p1w5c3'),
        (u'/', 317, 'p1w5c4'),
        (u'\xe6', 318, 'p1w5c5'),
        (u'n', 319, 'p1w5c6'),
        (u'i', 320, 'p1w5c7'),
        (u'd', 321, 'p1w5c8'),
        (u' ', 322, 'p1w6'),
        (u'"', 323, 'p1w6'),
        (u'd', 324, 'p1w6c1'),
        (u'u', 325, 'p1w6c2'),
        (u'c', 326, 'p1w6c3'),
        (u'k', 327, 'p1w6c4'),
        (u'"', 328, 'p1w6c5'),
        (u',', 329, 'p1w6c6'),
        (u' ', 330, 'p1w7'),
        # ...
        (u'A', 654, 'p1w54'),
        (u'n', 655, 'p1w54c1'),
        (u'c', 656, 'p1w54c2'),
        (u'i', 657, 'p1w54c3'),
        (u'e', 658, 'p1w54c4'),
        (u'n', 659, 'p1w54c5'),
        (u't', 660, 'p1w54c6'),
        (u' ', 661, 'p1w55'),
        (u'G', 662, 'p1w55'),
        (u'r', 663, 'p1w55c1'),
        (u'e', 664, 'p1w55c2'),
        (u'e', 665, 'p1w55c3'),
        (u'k', 666, 'p1w55c4'),
        (u' ', 667, 'p1w56'),
        (u'n', 668, 'p1w56'),
        (u'\u0113', 669, 'p1w56c1'),
        (u's', 670, 'p1w56c2'),
        (u's', 671, 'p1w56c3'),
        (u'a', 672, 'p1w56c4'),
        (u'/', 673, 'p1w56c5'),
        (u'n', 674, 'p1w56c6'),
        (u'\u0113', 675, 'p1w56c7'),
        (u't', 676, 'p1w56c8'),
        (u't', 677, 'p1w56c9'),
        (u'a', 678, 'p1w56c10'),
        (u' ', 679, 'p1w57'),
        (u'(', 680, 'p1w57'),
        (u'\u03bd', 681, 'p1w57c1'),
        (u'\u1fc6', 682, 'p1w57c2'),
        (u'\u03c3', 683, 'p1w57c3'),
        (u'\u03c3', 684, 'p1w57c4'),
        (u'\u03b1', 685, 'p1w57c5'),
        (u',', 686, 'p1w57c6'),
        (u' ', 687, 'p1w58'),
        (u'\u03bd', 688, 'p1w58'),
        (u'\u1fc6', 689, 'p1w58c1'),
        (u'\u03c4', 690, 'p1w58c2'),
        (u'\u03c4', 691, 'p1w58c3'),
        (u'\u03b1', 692, 'p1w58c4'),
        (u')', 693, 'p1w58c5'),
        (u' ', 694, 'p1w59'),
        # next paragraph
        (u'\n', 747, 'p2'),
        (u'\n', 748, 'p2'),
        (u'A', 749, 'p2'),
        (u' ', 750, 'p2w1'),
        (u'd', 751, 'p2w1'),
        (u'u', 752, 'p2w1c1'),
    ]

    def test_indexToPoint(self):
        """
        Given an integer index, a Point should be returned.
        """
        citer = Citer()
        for c,i,e in self.point_expectations:
            actual = citer.indexToPoint(self.original, i)
            self.assertEqual(e, actual,
                "Expected character at index {i}"
                " ({c!r}) to have citation {e!r}"
                " but it was actually {actual!r}".format(**locals()))

    def test_pointToIndex(self):
        """
        Given a Point citation, return an integer index.
        """
        citer = Citer()
        for c,i,p in self.point_expectations:
            actual = citer.pointToIndex(self.original, p)
            self.assertEqual(i, actual,
                "Expected index of {p} ({c!r})"
                " to be {i} but it was actually"
                " {actual!r}".format(**locals()))
