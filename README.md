[![Build Status](https://secure.travis-ci.org/iffy/tcite.png?branch=master)](http://travis-ci.org/iffy/tcite)

Suppose you have a text document, and you want to tag portions of it.  This is a format for doing that.

# Components

The format is made of the following:

- Points
- Ranges
- Selections

To describe those, refer to this sample text:

> I am a sample text.  I am a very simple piece of text for sample purposes.
>
> Don't think of me as something more than just a sample.
>
> I'm not one of those "meaningful" bits of text.


## Points

XXX Someone help with a formal specification, please.

A Point is a single place in the text and is used to make Ranges.  It is made of addition and subtraction of paragraphs and words.  There is also an *end-of* indicator (`e`).

Here's a table of examples using the sample text above.  The `*` in the *Example* indicates where the Point refers to:

| Point      | Meaning                                                      | Example |
|------------|--------------------------------------------------------------|---------|
| `p0`       | Start of the first paragraph                                 | "`*`I am a sample text..." |
| `p1`       | Start of the second paragraph                                | "`*`Don't think of me..." |
| `w2`       | Start of third word                                          | "I am `*`a sample text..." |
| `c2`       | Start of the third character                                 | "I `*`am a sample text..." |
| `p1+w1`    | Start of second word in second paragraph                     | "Don't `*`think of me..." |
| `p1+w1+c2` | Start of third character in second word of second paragraph  | "Don't th`*`ink of me..." |
| `p0e`      | End of first paragraph                                       | "...of text for sample purposes.`*`" |
| `p0e-w1`   | Start of second to last word in first paragraph              | "...of text for `*`sample purposes." |
| `p0e-w1e`  | End of second to last word in first paragraph                | "...of text for sample`*` purposes." |

### Normalized points

Points are considered *Normalized* if the following are all true:

1. No subtraction is used `-`
2. There is at most one *end-of* indicator (`e`)


## Ranges

A range is two points separated by `_`.  If the second Point is relative to the first Point, you may start the second Point with a `+` or `-` to indicate that.

So `p0_p0e-w3` refers to the range of text from the start of the first paragraph to the start of the 4th to last word from the end of the first paragraph.  In other words, this section of text (from the sample paragraph above):

> I am a sample text.  I am a very simple piece of 

The normalized version of this range is `p0_+w12`

## Selections

A Selection is one or more Ranges separated by `,`.  A single Range is also a Selection.

Suppose we had this original text:

> I am very glad to not have to be the only one talking with you about brains.

And we wanted to misquote the following from it:

> I am ... the only one ... with ... brains.

We could express that with the following selection:

`p0_+w1e,w9_+w2e,w13_+w0e,w16_+w0e`

If we only wanted to quote this:

> I am very glad...

That would be expressed with the following selection:

`p0_+w3e`


# World Languages

Many people use languages that aren't composed of characters and words in the same way that English is.  This can handle that as long as the encoding of the text is known.  (XXX perhaps this is an ignorant statement :)