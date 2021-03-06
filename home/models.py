from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.blocks import RawHTMLBlock



class HomePage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        # Add extra variables and return the updated context
        context['blog_entries'] = BlogPage.objects.live()
        return context    

class BlogPage(Page):
    kv = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    subtitle = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('rawhtml', RawHTMLBlock()),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('kv'),
        FieldPanel('subtitle'),
        FieldPanel('date'),
        StreamFieldPanel('body'),

    ]
