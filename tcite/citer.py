import re
from parsley import makeGrammar

r_newline = re.compile(r'[\n\r]+')
r_parabreak = re.compile(r'(\s*[\r\n]\s*[\r\n]\s*)', re.M | re.S)

word_delim = ' \t\r\n'

grammar_str = '''
digit = anything:x ?(x in '0123456789') -> x
number = <digit+>:ds -> int(''.join(ds))

escapedChar = ('\\{' -> '{') | ('\\}' -> '}')
pattern_string = (escapedChar | ~'}' anything)*:c -> ''.join(c)
pattern = '{' pattern_string:c '}' number?:count -> (c, count)

point = ('p' number)?:p pattern?:pat 'e'?:end
    -> Point(p, pat, end)

range = point:a '_' point:b -> (a, b)
'''
def _pointMaker(p, pat, end):
    pattern = ''
    count = 0
    if pat:
        pattern = pat[0]
        count = pat[1] or 0
    return Point(p, pattern, count, bool(end))

grammar = makeGrammar(grammar_str, {
    'Point': _pointMaker,
})


class Point(object):

    def __init__(self, p=None, pattern='', pattern_count=0, end=False):
        self.p = p
        self.pattern = pattern or ''
        self.pattern_count = pattern_count or 0
        self.end = end or False

    def isRelative(self):
        """
        Can this point be considered relative?
        """
        return self.p is None

    def __unicode__(self):
        parts = []
        if self.p is not None:
            parts.append('p{0}'.format(self.p))
        if self.pattern:
            pattern = self.pattern.replace('{', '\\{').replace('}', '\\}')
            parts.append(u'{{{0}}}'.format(pattern))
        if self.pattern_count:
            parts.append(str(self.pattern_count))
        if self.end:
            parts.append('e')
        return ''.join(parts)

    def __repr__(self):
        return unicode(self)

def splitws(s):
    """
    Trim whitespace from front an back of string and return a tuple
    of leading ws, string, trailing ws.
    """
    length = len(s)
    original = s
    s = s.lstrip()
    leading = original[:length-len(s)]
    length = len(s)
    s = s.rstrip()
    trailing = original[-length-len(s):]
    return leading, s, trailing


class Citer(object):

    def splitWords(self, text):
        """
        Split a piece of text into words.
        """
        return filter(None, [x.strip() for x in text.split()]) or ['']

    def splitParagraphs(self, text):
        """
        Split text into paragraphs delimited by two or more lines of whitespace
        """
        broken = r_parabreak.split(text)
        offset = 0
        for chunk in broken:
            isbreak = r_parabreak.match(chunk) is not None
            if chunk and not isbreak:
                yield chunk, offset
            offset += len(chunk)


    def indexToPoint(self, text, index):
        """
        Given an index in a string, return the point citation.
        """
        if abs(index) > len(text):
            raise IndexError(index, text)

        if index < 0:
            index = len(text) + index

        np = 0
        pattern = ''
        count = 0
        end = False

        i = 0
        last_np = 0
        last_p = ''
        last_offset = 0
        for p, offset in self.splitParagraphs(text):
            if index < offset:
                if last_p:
                    # it was the last paragraph
                    pass
                else:
                    # special case first paragraph
                    last_p = p
                    last_offset = offset
                    last_np = i
                break
            last_p = p
            last_offset = offset
            last_np = i
            i += 1

        p = last_p
        offset = last_offset
        np = last_np

        if index >= (offset + len(p)):
            # end of paragraph
            end = True
        elif index < offset:
            # start of paragraph
            pass
        else:
            # start/middle of paragraph
            head = p[:index-offset]
            if not head:
                # start of paragraph
                pass
            else:
                # middle of paragraph
                tail = p[index-offset:]


                start_of_word = True
                end_of_word = False
                if head:
                    start_of_word = head[-1] in word_delim
                if tail:
                    end_of_word = tail[0] in word_delim


                if start_of_word and end_of_word:
                    stripped_head = head.rstrip()
                    ws_part = head[len(stripped_head):]
                    nonws_part = stripped_head.split()[-1]
                    pattern = nonws_part + ws_part
                    end = True
                elif start_of_word:
                    pattern = tail.split()[0]
                    count = head.count(pattern)
                else:
                    pattern = head.split()[-1]
                    rest = head[:-len(pattern)]
                    count = rest.count(pattern)
                    end = True
        
        return Point(np, pattern, count, end)


    def pointToIndex(self, text, point):
        """
        Given a point in a string, return the index of that point.
        """
        if isinstance(point, (str, unicode)):
            point = grammar(point).point()
        return self._pointObjectToIndex(text, point)


    def _pointObjectToIndex(self, text, point):
        p = text
        offset = 0
        if point.p is not None:
            # has paragraph designation
            paragraphs = list(self.splitParagraphs(text))
            p, offset = paragraphs[point.p]
        
        if point.pattern:
            # pattern
            index = offset
            pattern_index = 0
            for i in xrange(point.pattern_count):
                pattern_index = p.index(point.pattern, pattern_index) + len(point.pattern)
            index += p.index(point.pattern, pattern_index)
            if point.end:
                index += len(point.pattern)
            return index
        else:
            # just paragraph
            if point.end:
                return offset + len(p)
            else:
                return offset


    def rangeToIndex(self, text, trange):
        """
        Convert a range string to a range index tuple.
        """
        data = grammar(trange).range()
        start = self._pointObjectToIndex(text, data[0])
        end = None
        if data[1].isRelative():
            end = self._pointObjectToIndex(text[start:], data[1]) + start
        else:
            end = self._pointObjectToIndex(text, data[1])
        return (start, end)


    def indexToRange(self, text, index):
        """
        Convert a range index tuple to a range string.
        """
        start = self.indexToPoint(text, index[0])
        end = self.indexToPoint(text, index[1])
        return u'{start}_{end}'.format(**locals())


