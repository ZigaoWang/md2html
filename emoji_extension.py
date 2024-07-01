import markdown
from markdown.inlinepatterns import InlineProcessor
from xml.etree import ElementTree as etree
import emoji

EMOJI_PATTERN = r'(:[a-zA-Z0-9_]+:)'

class EmojiExtension(markdown.Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(EmojiPattern(EMOJI_PATTERN, md), 'emoji', 175)

class EmojiPattern(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('span')
        el.text = emoji.emojize(m.group(1), language='alias')
        return el, m.start(0), m.end(0)

def makeExtension(**kwargs):
    return EmojiExtension(**kwargs)