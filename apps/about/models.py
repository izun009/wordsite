from django.db import models

from wagtail.search import index
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from ..pages.blocks import AboutStreamBlock
from ..blog.models import PostCategory

# About Page
class AboutPage(Page):

    templates = 'about/about_page.html'
    max_count = 1

    body = StreamField(
        AboutStreamBlock(), verbose_name="About Page", blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('title'),
    ]

    subpage_types = []

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'

    def get_context(self, request):
        context = super(AboutPage, self).get_context(request)
        context['categories'] = PostCategory.objects.all()
        return context