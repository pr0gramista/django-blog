import logging
import re

from django.template import engines
from mistune import Renderer, InlineLexer

logger = logging.getLogger(__name__)

class PostRenderer(Renderer):
    def figure(self, text, link, alt):
        return '<figure><img src="%s" alt="%s" /><div>%s</div></figure>' % (link, alt, text)

    def emdash(self):
        return '\u2014'

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

    def gallery(self, links):
        gallery_template = """
        <div class="gallery less">
          <div class="gallery-content mdl-grid">
            <div class="gallery-shadow"></div>
            {% for link in links %}
            <div class="mdl-cell mdl-cell--4-col">
              <img src="{{ link }}">
            </div>
            {% endfor %}
          </div>
          <div class="gallery-more">
            <button><i class="material-icons">expand_more</i></button>
          </div>
          <div class="gallery-less">
            <button><i class="material-icons">expand_less</i></button>
          </div>
        </div>
        """

        django_engine = engines['django']
        return django_engine.from_string(gallery_template).render({
            'links': links
        })


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

    def enable_emdash(self):
        self.rules.emdash = re.compile(
            r'!--'
        )
        self.default_rules.insert(3, 'emdash')

    def output_emdash(self, m):
        return self.renderer.emdash()

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

    def enable_gallery(self):
        self.rules.gallery = re.compile(r'Gallery\[(.*)\]')
        self.default_rules.insert(3, 'gallery')

    def output_gallery(self, m):
        inside = m.group(1)

        return self.renderer.gallery([link.strip() for link in inside.split(',')])
