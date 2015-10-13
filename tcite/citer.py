import re
r_newline = re.compile(r'[\n\r]+')

word_delim = ' \t'
para_delim = '\r\n'

class Citer(object):

    def splitWords(self, text):
        """
        Split a piece of text into words.
        """
        return filter(None, [x.strip() for x in text.split()]) or ['']

    def splitParagraphs(self, text):
        lines = (x.strip() for x in text.replace('\r', '\n').split('\n'))
        non_empty_lines = (x for x in lines if x)
        return list(non_empty_lines)

    def indexToPoint(self, text, index):
        """
        Given an index in a string, return the point citation.
        """
        print 'indexToPoint(%r, %r)' % (text, index)
        if abs(index) > len(text):
            raise IndexError(index, text)
        np = 0
        pattern = ''
        end = False
        count = 0

        head = text[:index]
        tail = text[index:]
        print 'head', repr(head)
        print 'tail', repr(tail)

        # count the leading paragraphs
        paragraphs = self.splitParagraphs(head)
        print 'paragraphs', paragraphs
        

        if tail and tail[0] in para_delim:
            # end of paragraph
            print 'end of paragraph'
            if paragraphs:
                np = len(paragraphs) - 1
                end = True
        elif (head and head[-1] in para_delim) or not head.strip():
            # start of paragraph
            print 'start of paragraph'
            np = len(paragraphs)
        else:
            # middle of paragraph
            print 'middle of paragraph'
            if paragraphs:
                np = len(paragraphs) - 1
            print 'head', repr(head)
            print 'tail', repr(tail)

            start_of_word = True
            end_of_word = False
            if head:
                start_of_word = head[-1] in word_delim
            if tail:
                end_of_word = tail[0] in word_delim

            if start_of_word and end_of_word:
                print 'middle of whitespace'
                stripped_head = head.rstrip()
                ws_part = head[len(stripped_head):]
                nonws_part = stripped_head.split()[-1]
                pattern = nonws_part + ws_part
                end = True
            elif start_of_word:
                print 'start of word'
                pattern = tail.split()[0]
                count = head.count(pattern)
            else:
                print 'mid/end of word'
                pattern = head.split()[-1]
                rest = head[:-len(pattern)]
                print 'looking in', repr(rest), 'for', repr(pattern)
                count = rest.count(pattern)
                end = True

        parts = []
        parts.append('p{}'.format(np))
        if pattern:
            parts.append(u'{{{}}}'.format(pattern))
        if count:
            parts.append(str(count))
        if end:
            parts.append('e')

        return ''.join(parts)

    def pointToIndex(self, text, point):
        """
        Given a point in a string, return the index of that point.
        """


    def rangeFromText(self, text, sample):
        """
        Given a text and a sample from the text, produce a range citation.
        """
        index = text.index(sample)
        pointer = index

        # start paragraph
        paragraphs = self.splitParagraphs(text)
        start_p = 0
        for p in paragraphs:
            if len(p) <= pointer:
                pointer -= len(p)
                start_p += 1

        # start word
        if pointer:
            text_words = self.splitWords(p)

        # Find end

        end_w = len(sample.split()) - 1


        print 'pointer', pointer

        return 'p{start_p}_+w{end_w}e'.format(**locals())