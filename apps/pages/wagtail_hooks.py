import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.core import hooks

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from ..blog.models import PostCategory, PostPage

"""
Liat dokumentasi wagtail hooks untuk kustomisasi richtext dan lainnya.
"""

# Wagtail ModelAdmin
class PostPageModelAdmin(ModelAdmin):
    model = PostPage
    menu_label = 'All Posts'
    menu_icon = 'folder-inverse'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('title', 'category', 'tag', 'first_published_at')
    list_filter = ('categories',)
    search_fields = ('title', 'categories')

    # def categories(self, obj):
    #     return "\n".join([p.title for p in self.categories.all()])

    def category(self, obj):

        category = ", \n".join([
            p.title for p in obj.categories.all()
        ])
        # return ", \n".join([p.title for p in obj.categories.all()])
        return category

    def tag(self, obj):

        tag = ", \n".join([
            p.name for p in obj.tags.all()
        ])
        return tag

modeladmin_register(PostPageModelAdmin)

# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'mark'
    type_ = 'MARK'
    tag = 'mark'

    control = {
        'type': type_,
        'label': '☆',
        'description': 'Mark',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    features.register_converter_rule('contentstate', feature_name, db_conversion)
    
    features.default_features.append(feature_name)

# Adding Code in RichText
@hooks.register("register_rich_text_features")
def register_code_styling(features):
    """Add the <code> to the richtext editor and page."""

    feature_name = "code"
    type_ = "PRE"
    tag = "pre"

    control = {
        "type": type_,
        "label": "</>",
        "description": "Code"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)

# Adding Subscript in RichText
@hooks.register("register_rich_text_features")
def register_subscript_styling(features):
    """Add the <subscript> to the richtext editor and page."""

    feature_name = "subscript"
    type_ = "SUB"
    tag = "sub"

    control = {
        "type": type_,
        # "label": "X₁",
        "description": "Subscript"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)

# Adding Supscript in RichText
@hooks.register("register_rich_text_features")
def register_superscript_styling(features):
    """Add the <superscript> to the richtext editor and page."""

    feature_name = "superscript"
    type_ = "SUP"
    tag = "sup"

    control = {
        "type": type_,
        # "label": "X¹",
        "description": "Superscript"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)

# Adding Strikethrough in RichText
@hooks.register("register_rich_text_features")
def register_strikethrough_styling(features):
    """Add the <strikethrough> to the richtext editor and page."""

    feature_name = "strikethrough"
    type_ = "DEL"
    tag = "del"

    control = {
        "type": type_,
        #"label": "S",
        "description": "Strikethrough"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)

# Adding Underline in RichText
@hooks.register("register_rich_text_features")
def register_underline_styling(features):
    """Add the <underline> to the richtext editor and page."""

    feature_name = "underline"
    type_ = "UNDERLINE"
    tag = "u"

    control = {
        "type": type_,
        "label": "U",
        "description": "Underline"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)

# Adding Blockquote in RichText
@hooks.register("register_rich_text_features")
def register_blockquote_styling(features):
    """Add the <blockquote> to the richtext editor and page."""

    feature_name = "blockquote"
    type_ = "BLOCKQUOTE"
    tag = "blockquote"

    control = {
        "type": type_,
        #"label": "",
        "description": "Blockquote"
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)


