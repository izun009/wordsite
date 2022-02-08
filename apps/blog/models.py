from __future__ import unicode_literals

# Django Library
from django import forms
from django.db import models
from django.http import Http404
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Wagtail Library
from wagtail.search import index
from wagtail.search.models import Query
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel

# Additional Library
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import Tag as TaggitTag, TaggedItemBase

from ..pages.blocks import BaseStreamBlock

# Snippet Author
@register_snippet
class BlogAuthor(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    intro = models.TextField(blank=False, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("intro"),
                ImageChooserPanel("image"),
            ],
            heading="Author Profile",
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:  # noqa
        verbose_name = "Author"
        verbose_name_plural = "Authors"


# Snippet Category
@register_snippet
class PostCategory(models.Model):
    title = models.CharField(max_length=50, blank=False, null=True)
    introduction = models.TextField(blank=False, null=True)
    slug = models.SlugField(
        verbose_name='slug', allow_unicode=True, max_length=255)

    panels = [
        FieldPanel("title"),
        FieldPanel("introduction"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

# Snippet Tags
@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items', on_delete=models.CASCADE)

# Related Post based on Tags
class BlogPostManager(PageManager):

    def related_posts(self, post, max_items=3):
        tags = post.tags.all()

        matches = BlogPost.objects.filter(tags__in=tags).live().annotate(Count('title'))
        matches = matches.exclude(pk=post.pk)

        related = matches.order_by('-title__count')
        return related[:max_items]

# Post Page
class BlogPost(Page):

    templates = 'blog/blog_post.html'

    # Related Post based on Tags
    relatetags = BlogPostManager()

    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    author = models.ForeignKey(
        "BlogAuthor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    date_published = models.DateField(
        "Date published", blank=False, null=True
    )
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    categories = ParentalManyToManyField('PostCategory', blank=False)

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('blog_image'),            
            FieldPanel('author'),
            FieldPanel('date_published'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ],heading="Blog Info",),
        
        StreamFieldPanel('body'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('tags'),
        index.SearchField('categories'),
    ]

    parent_page_types = ['BlogPage']
    subpage_types = []

    class Meta:
        ordering = ['-first_published_at',]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_context(self, request):
        context = super(BlogPost, self).get_context(request)
        context['related_posts'] = BlogPost.relatetags.related_posts(self)[:3]
        context['categories'] = PostCategory.objects.all().annotate(posts_count=Count('blogpost'))
        context['all_tags'] = Tag.objects.all()
        return context

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tag',
                tag.slug
            ])
        return tags
    

# blog Page
class BlogPage(RoutablePageMixin, Page):

    templates = 'blog/blog_page.html'
    max_count = 1

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    def get_context(self, request):
        context = super(BlogPage, self).get_context(request)
        context['posts'] = BlogPost.objects.descendant_of(self).live().order_by('-first_published_at')[:10]
        context['categories'] = PostCategory.objects.all().annotate(posts_count=Count('blogpost'))
        return context

    # Tags list
    @route(r'^tag/$', name='tag_archive')
    @route(r'^tag/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            return redirect(self.url)
        
        posts = self.get_posts(tag=tag)
        pagination = Paginator(posts, 10)
        page = request.GET.get("page")

        try:
            posts = pagination.page(page)
        except PageNotAnInteger:
            posts = pagination.page(1)
        except EmptyPage:
            posts = pagination.page(pagination.num_pages)

        categories = PostCategory.objects.all().annotate(posts_count=Count('blogpost'))
        all_tags = Tag.objects.all()

        context = {
            'tag': tag,
            'posts': posts,
            'all_tags':all_tags,
            'categories':categories,
        }
        return render(request, 'blog/blog_category_and_tag.html', context)
        
    def serve_preview(self, request, mode_name):
        return self.serve(request)

    def get_posts(self, tag=None, cat=None):
        posts = BlogPost.objects.live().descendant_of(self).order_by('-first_published_at')
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags

    # Category View
    @route(r'^category/$', name='category_view')
    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug=None):
        context = self.get_context(request)

        try:
            category = PostCategory.objects.get(slug=cat_slug)
        except PostCategory.DoesNotExist:
            return redirect(self.url)

        self.title = category.title
        self.introduction = category.introduction

        all_category_posts = BlogPost.objects.filter(
            categories__in=[category],
        ).descendant_of(self).live().order_by('-first_published_at')
        pagination = Paginator(all_category_posts, 10)
        page = request.GET.get("page")

        try:
            posts = pagination.page(page)
        except PageNotAnInteger:
            posts = pagination.page(1)
        except EmptyPage:
            posts = pagination.page(pagination.num_pages)

        context["posts"] = posts
        context["pagination"] = pagination
        return render(request, "blog/blog_category_and_tag.html", context)


    # Search View    
    @route(r"^s/$", name="search_view")
    def search_view(self, request):

        search_query = request.GET.get('q', None)
        page = request.GET.get('page', 1)

        # Search
        if search_query:
            search_results = BlogPost.objects.live().order_by('-first_published_at').search(search_query)
            query = Query.get(search_query)

            # Record hit
            query.add_hit()
        else:
            search_results = BlogPost.objects.none()

        # Pagination
        paginator = Paginator(search_results, 10)
        try:
            search_results = paginator.page(page)
        except PageNotAnInteger:
            search_results = paginator.page(1)
        except EmptyPage:
            search_results = paginator.page(paginator.num_pages)

        categories = PostCategory.objects.all().annotate(posts_count=Count('blogpost'))
        all_tags = Tag.objects.all()

        context = {
            'search_query': search_query,
            'search_results': search_results,
            'categories':categories,
            'all_tags':all_tags,
        }

        return render(request, 'blog/search_page.html', context)
