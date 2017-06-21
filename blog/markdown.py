import re
from mistune import Renderer, InlineGrammar, InlineLexer


class FigureRenderer(Renderer):
    def figure(self, text, link, alt):
        return '<figure><img src="%s" alt="%s" /><div>%s</div></figure>' % (link, alt, text)


class FigureInlineLexer(InlineLexer):
    def enable_figure(self):
        self.rules.figure = re.compile(
            r'!\[(.*)\]\[(.*)\]\((.*)\)'
        )
        self.default_rules.insert(3, 'figure')

    def output_figure(self, m):
        text = m.group(1)
        alt = m.group(2)
        link = m.group(3)
        return self.renderer.figure(text, link, alt)
