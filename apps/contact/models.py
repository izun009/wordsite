from django.db import models

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)

from ..blog.models import PostCategory

class FormField(AbstractFormField):
    page = ParentalKey("ContactPage", related_name="custom_form_fields")


class ContactPage(WagtailCaptchaEmailForm):

    max_count = 1

    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel("custom_form_fields", label="Form fields"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email Notification Config",
        ),
    ]

    subpage_types = []

    def get_context(self, request):
        context = super(ContactPage, self).get_context(request)
        context['categories'] = PostCategory.objects.all()
        return context

    def get_form_fields(self):
        return self.custom_form_fields.all()