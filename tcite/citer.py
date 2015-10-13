import re
from parsley import makeGrammar

r_newline = re.compile(r'[\n\r]+')

word_delim = ' \t'
para_delim = '\r\n'

grammar_str = '''
digit = anything:x ?(x in '0123456789') -> x
number = <digit+>:ds -> int(''.join(ds))

escapedChar = ('\\{' -> '{') | ('\\}' -> '}')
pattern_string = (escapedChar | ~'}' anything)*:c -> ''.join(c)
pattern = '{' pattern_string:c '}' number?:count -> (c, count)

point = ('p' number)?:p pattern?:pat 'e'?:end
    -> {
        'p':p,
        'pattern':pat,
        'end': bool(end),
    }
'''
grammar = makeGrammar(grammar_str, {})


class Point(object):

    def __init__(self, p=0, pattern='', pattern_count=0, end=False):
        self.p = p or 0
        self.pattern = pattern or ''
        self.pattern_count = pattern_count or 0
        self.end = end or False

    def __unicode__(self):
        parts = []
        parts.append('p{}'.format(self.p))
        if self.pattern:
            pattern = self.pattern.replace('{', '\\{').replace('}', '\\}')
            parts.append(u'{{{}}}'.format(pattern))
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

    def splitParagraphs(self, text, with_offsets=False):
        lines = (x for x in text.replace('\r', '\n').split('\n'))
        if with_offsets:
            offset = 0
            for line in lines:
                leading, s, trailing = splitws(line)
                offset += len(leading)
                if s:
                    yield s, offset
                offset += len(trailing)
                offset += 1 # for terminal \n
        else:
            for line in lines:
                line = line.strip()
                if line:
                    yield line

    def indexToPoint(self, text, index):
        """
        Given an index in a string, return the point citation.
        """
        if abs(index) > len(text):
            raise IndexError(index, text)

        np = 0
        pattern = ''
        count = 0
        end = False

        head = text[:index]
        tail = text[index:]

        # count the leading paragraphs
        paragraphs = list(self.splitParagraphs(head))
        

        if tail and tail[0] in para_delim:
            # end of paragraph
            if paragraphs:
                np = len(paragraphs) - 1
                end = True
        elif (head and head[-1] in para_delim) or not head.strip():
            # start of paragraph
            np = len(paragraphs)
        else:
            # middle of paragraph
            if paragraphs:
                np = len(paragraphs) - 1

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
        data = grammar(point).point()
        pattern = ''
        count = 0
        if data['pattern']:
            pattern = data['pattern'][0]
            count = data['pattern'][1] or 0
        parsed = Point(data['p'], pattern, count, data['end'])


        paragraphs = list(self.splitParagraphs(text, with_offsets=True))
        p, offset = paragraphs[parsed.p]
        if parsed.pattern:
            # pattern
            index = offset
            pattern_index = 0
            for i in xrange(parsed.pattern_count):
                pattern_index = p.index(parsed.pattern, pattern_index) + len(parsed.pattern)
            index += p.index(parsed.pattern, pattern_index)
            if parsed.end:
                index += len(parsed.pattern)
            return index
        else:
            # just paragraph
            if parsed.end:
                return offset + len(p)
            else:
                return offset

