import re
from mistune import Renderer, InlineGrammar, InlineLexer


class PostRenderer(Renderer):
    def figure(self, text, link, alt):
        return '<figure><img src="%s" alt="%s" /><div>%s</div></figure>' % (link, alt, text)

    def woo(self, text, link, icon, color, clazz):
        return '''
               <div class="woo">
                 <div class="woo-fake" style="background: #%s;"></div>
                   <a href="%s"><div class="woo-content-wrapper">
                     <div class="woo-content %s">
                     <i class="material-icons">%s</i>
                     <div>%s</div>
                   </div>
                 </div></a>
               </div>
               ''' % (color, link, clazz, icon, text)


class PostInlineLexer(InlineLexer):
    def enable_woo(self):
        # Syntax for 'woo' element
        # !F[text][icon name][color without #][class (can be empty)](link)
        self.rules.woo = re.compile(
            r'!F\[(.*)\]\[(.*)\]\[(.*)\]\[(.*)\]\((.*)\)'
        )
        self.default_rules.insert(3, 'woo')

    def output_woo(self, m):
        text = m.group(1)
        icon = m.group(2)
        color = m.group(3)
        clazz = m.group(4)
        link = m.group(5)
        return self.renderer.woo(text=text, icon=icon, color=color, clazz=clazz, link=link)

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
