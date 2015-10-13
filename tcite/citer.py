word_delim = set(' \t')
para_delim = set('\r\n')

class Citer(object):

    def splitParagraphs(self, text):
        """
        Split a text into a list of paragraphs.
        """
        return filter(None, [x.strip() for x in text.split('\n')]) or ['']

    def splitWords(self, text):
        """
        Split a piece of text into words.
        """
        return filter(None, [x.strip() for x in text.split()]) or ['']

    def indexToPoint(self, text, index):
        """
        Given an index in a string, return the point citation.
        """
        np = 0
        nw = 0
        nc = 0

        head = text[:index] or ' '
        if not head.strip():
            # special case start of string
            return 'p0'

        tail = text[index:] or ' '
        word_boundary = head[-1] in word_delim or tail[0] in word_delim
        para_boundary = head[-1] in para_delim or tail[0] in para_delim

        # number of paragraphs
        paragraphs = self.splitParagraphs(head)
        if para_boundary:
            np = len(paragraphs)
        else:
            np = len(paragraphs) - 1

            # words
            head = paragraphs[-1]
            words = self.splitWords(head)

            if word_boundary:
                nw = len(words)
            else:
                nw = len(words) - 1
                nc = len(words[-1])

        parts = []
        if np:
            parts.append('p{}'.format(np))
        if nw:
            parts.append('w{}'.format(nw))
        if nc:
            parts.append('c{}'.format(nc))

        if not parts:
            parts = ['p0']
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