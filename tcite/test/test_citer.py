# -*- coding: utf-8 -*-
from twisted.trial.unittest import TestCase


from tcite.citer import Citer


class CiterTest(TestCase):

    def assertPoint(self, text, index, point, reverse=True):
        """
        Assert that the given index within the given text produces the
        expected point
        """
        citer = Citer()
        actual = citer.indexToPoint(text, index)
        self.assertEqual(point, unicode(actual),
            u"Expected index {index} to"
            u" be at point {point} but it was {actual}"
            u"\n\n{text!r}".format(**locals()).encode('utf-8'))

        if reverse:
            # assert the reverse
            self.assertIndex(text, point, index)

    def assertIndex(self, text, point, expected_index):
        """
        Assert that the given point resolves to the expected_index.
        """
        citer = Citer()
        actual = citer.pointToIndex(text, point)
        self.assertEqual(actual, expected_index,
            u"Expected point {point} to"
            u" be converted to index {expected_index} but it was {actual}"
            u"\n\n{text!r}".format(**locals()).encode('utf-8'))

    def test_start_with_whitespace(self):
        self.assertPoint('\n\n\nfoo bar baz\n\n', 0, 'p0', reverse=False)
        self.assertPoint('\n\n\nfoo bar baz\n\n', 1, 'p0', reverse=False)
        self.assertPoint('\n\n\nfoo bar baz\n\n', 2, 'p0', reverse=False)
        self.assertPoint('\n\n\nfoo bar baz\n\n', 3, 'p0')

    def test_start_no_whitespace(self):
        self.assertPoint('foo bar baz', 0, 'p0')

    def test_second_paragraph(self):
        self.assertPoint('\n\nfoo\nbar', 6, 'p1')
        self.assertPoint('foo\nbar', 4, 'p1')
        self.assertPoint('\n\nfoo\n\n\nbar', 8, 'p1')
        self.assertPoint('\n\nfoo\n\n\nbar', 5, 'p0e')
        self.assertPoint('\n\nfoo\n\n\nbar', 7, 'p0e', reverse=False)
        self.assertPoint('\n\rfoo\r\n\rbar', 8, 'p1')
        self.assertPoint('\n\rfoo\r\n\rbar', 9, 'p1{b}e')
        self.assertPoint('\n\rfoo\r\n\rbar', 7, 'p0e', reverse=False)

    def test_start_of_word(self):
        self.assertPoint('foo bar baz', 4, 'p0{bar}')
        self.assertPoint('foo bar baz', 8, 'p0{baz}')
        self.assertPoint('foo bar baz', 0, 'p0')

    def test_middle_of_word(self):
        self.assertPoint('alligator and friends', 1, 'p0{a}e')
        self.assertPoint('alligator and friends', 2, 'p0{al}e')
        self.assertPoint('alligator and friends', 3, 'p0{all}e')
        self.assertPoint('alligator and friends', 4, 'p0{alli}e')
        self.assertPoint('alligator and friends', 5, 'p0{allig}e')

    def test_end_of_word(self):
        self.assertPoint('alligator and friends', 9, 'p0{alligator}e')
        self.assertPoint('alligator and friends', 13, 'p0{and}e')

    def test_unicode(self):
        self.assertPoint(u'nēssa/nētta (νῆσσα, νῆττα)', 0, u'p0')
        self.assertPoint(u'nēssa/nētta (νῆσσα, νῆττα)', 11,
            u'p0{nēssa/nētta}e')
        self.assertPoint(u'nēssa/nētta (νῆσσα, νῆττα)', 12,
            u'p0{(νῆσσα,}')

    def test_curly(self):
        self.assertPoint('foo {foo} foo', 4, 'p0{\\{foo\\}}')
        self.assertPoint('foo {foo foo', 4, 'p0{\\{foo}')
        self.assertPoint('foo foo} foo', 4, 'p0{foo\\}}')
        self.assertPoint('foo { foo', 4, 'p0{\\{}')
        self.assertPoint('foo } foo', 4, 'p0{\\}}')

    def test_middleOfWhitespace(self):
        self.assertPoint('foo   foo ', 4, 'p0{foo }e')
        self.assertPoint('foo   foo ', 5, 'p0{foo  }e')
        self.assertPoint('foo  \t \t foo ', 0, 'p0')
        self.assertPoint('foo  \t \t foo ', 1, 'p0{f}e')
        self.assertPoint('foo  \t \t foo ', 2, 'p0{fo}e')
        self.assertPoint('foo  \t \t foo ', 3, 'p0{foo}e')
        self.assertPoint('foo  \t \t foo ', 4, 'p0{foo }e')
        self.assertPoint('foo  \t \t foo ', 5, 'p0{foo  }e')
        self.assertPoint('foo  \t \t foo ', 6, 'p0{foo  \t}e')
        self.assertPoint('foo  \t \t foo ', 7, 'p0{foo  \t }e')
        self.assertPoint('foo  \t \t foo ', 8, 'p0{foo  \t \t}e')
        self.assertPoint('foo  \t \t foo ', 9, 'p0{foo}1')
        self.assertPoint('a b   c   d e', 4, 'p0{b }e')

    def test_end_of_last_paragraph(self):
        self.assertPoint('foo\nbar\nbaz\n\n', 11, 'p2e')
        self.assertPoint('foo\nbar\nbaz\n\n', 12, 'p2e', reverse=False)

    def test_second_occurrence(self):
        self.assertPoint('foo foo foo foo', 0, 'p0')
        self.assertPoint('foo foo foo foo', 3, 'p0{foo}e')
        self.assertPoint('foo foo foo foo', 4, 'p0{foo}1')
        self.assertPoint('foo foo foo foo', 7, 'p0{foo}1e')
        self.assertPoint('foo foo foo foo', 8, 'p0{foo}2')
        self.assertPoint('foo foo foo foo', 11, 'p0{foo}2e')
        self.assertPoint('foo foo foo foo', 12, 'p0{foo}3')
        self.assertPoint('foo foo foo foo', 15, 'p0{foo}3e')

    def test_negative(self):
        self.assertPoint('foo\nbar\nbaz\n\n', -1, 'p2e', reverse=False)
        self.assertPoint('foo\nbar\nbaz\n\n', -3, 'p2{ba}1e', reverse=False)

    def test_beyond(self):
        citer = Citer()
        self.assertRaises(IndexError, citer.indexToPoint, 'foo', 400)
        self.assertRaises(IndexError, citer.indexToPoint, 'foo', -100)

    def test_chinese(self):
        # from http://generator.lorem-ipsum.info/
        text = u'''銈 焲犈 藙藨蠈 螏螉褩 雥齆犪, 灊灅 灊灅

慛 臡虈觿 翍脝艴 螒螝,'''
        self.assertPoint(text, 0, 'p0')
        self.assertPoint(text, 1, u'p0{銈}e')
        self.assertPoint(text, 13, u'p0{雥齆犪,}')
        self.assertPoint(text, 21, u'p0{灊灅}1')
        self.assertPoint(text, 27, u'p1{臡虈觿}')

    def test_noParagraph(self):
        """
        Points with no paragraph specified look over the whole document.
        """
        self.assertIndex('foo bar', '{bar}', 4)
        self.assertIndex('foo\nbar\nbaz', '{baz}', 8)
        self.assertIndex('foo\nfoo\nfoo', '{foo}1e', 7)


