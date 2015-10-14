# -*- coding: utf-8 -*-
from twisted.trial.unittest import TestCase


from tcite.citer import Citer


class CiterPointTest(TestCase):

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
        self.assertPoint('\n\nfoo\nbar', 6, 'p0{bar}')
        self.assertPoint('foo\nbar', 4, 'p0{bar}')
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
        self.assertPoint('foo\n\nbar\n\nbaz\n\n', 13, 'p2e')
        self.assertPoint('foo\n\nbar\n\nbaz\n\n', 14, 'p2e', reverse=False)

    def test_second_occurrence(self):
        self.assertPoint('foo foo foo foo', 0, 'p0')
        self.assertPoint('foo foo foo foo', 3, 'p0{foo}e')
        self.assertPoint('foo foo foo foo', 4, 'p0{foo}1')
        self.assertPoint('foo foo foo foo', 7, 'p0{foo}1e')
        self.assertPoint('foo foo foo foo', 8, 'p0{foo}2')
        self.assertPoint('foo foo foo foo', 11, 'p0{foo}2e')
        self.assertPoint('foo foo foo foo', 12, 'p0{foo}3')
        self.assertPoint('foo foo foo foo', 15, 'p0e')

    def test_negative(self):
        self.assertPoint('foo\n\nbar\n\nbaz\n\n', -1, 'p2e', reverse=False)
        self.assertPoint('foo\n\nbar\n\nbaz\n\n', -3, 'p2{ba}e', reverse=False)

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
        self.assertIndex('foo\n\nbar\n\nbaz', '{baz}', 10)
        self.assertIndex('foo\n\nfoo\n\nfoo', '{foo}1e', 8)


class CiterRangeTest(TestCase):

    def assertRangeToIndex(self, text, trange, expected_index):
        citer = Citer()
        actual = citer.rangeToIndex(text, trange)
        self.assertEqual(expected_index, actual,
            "Expected range {trange} to be index"
            " {expected_index} but it was actually {actual}"
            "\n\n{text!r}".format(**locals()))

    def assertIndexToRange(self, text, index, expected_range):
        citer = Citer()
        actual = citer.indexToRange(text, index)
        self.assertEqual(expected_range, actual,
            "Expected index {index} to be range"
            " {expected_range} but it was actually {actual}"
            "\n\n{text!r}".format(**locals()))        

    def test_basic(self):
        self.assertRangeToIndex('foo bar', '{foo}_{bar}e', (0, 7))
        self.assertRangeToIndex('foo bar', '{foo}e_{bar}e', (3, 7))

    def test_relativeToStart(self):
        self.assertRangeToIndex('dog foo dog', '{foo}_{dog}e', (4, 11))
        self.assertRangeToIndex('dog foo dog dog', '{foo}_{dog}1e', (4, 15))

    def test_absoluteParagraph(self):
        self.assertRangeToIndex('dog foo\n\ndog\n\ndog', '{foo}_p2{dog}e', (4, 17))
        self.assertRangeToIndex('dog foo\n\ndog\n\ndog', '{foo}_p2e', (4, 17))

    def test_spanParagraphs(self):
        self.assertRangeToIndex('a\n\nb\n\nc', '{a}_{c}e', (0, 7))

    def test_paragraph(self):
        self.assertRangeToIndex('a\n\nb\n\nc', 'p0_p2e', (0, 7))
        self.assertRangeToIndex('a\n\nb\n\nc', 'p1_p2e', (3, 7))

        self.assertIndexToRange('a\n\nb\n\nc', (0, 7), 'p0_p2e')
        self.assertIndexToRange('a\n\nb\n\nc', (3, 7), 'p1_p2e')

    def test_indexToRange_pattern(self):
        self.assertIndexToRange('a b c\n\nd e f', (2, 3), 'p0{b}_p0{b}e')
        self.assertIndexToRange('a b c\n\nd e f', (2, 9), 'p0{b}_p1{e}')
