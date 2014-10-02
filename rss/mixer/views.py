from django.core.cache import cache
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import FormView, RedirectView
from feedparser import parse
from itertools import chain

from forms import AddFeedForm


class MixerView(FormView):
    form_class = AddFeedForm
    success_url = '/'
    template_name = 'mixer/feed.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return JsonResponse(self.get_data(context), **response_kwargs)
        return super(MixerView, self).render_to_response(
            context, **response_kwargs)

    def get_data(self, context):
        """
        Returns the JSON serializable context that will be returned to an AJAX
        call
        """
        return dict(
            feed_list=context['feed_list'], feed_count=context['feed_count'],
            item_list=context['item_list'], item_count=context['item_count'])

    def get_context_data(self, **kwargs):
        feeds = cache.get('feeds', {})

        # Merge all feed entries and reverse sort them by publish date
        items = cache.get('items', {})
        items = sorted(chain.from_iterable(items.itervalues()),
                       key=lambda k: k.published_parsed, reverse=True)
        # We don't need the parsed date anymore, and since it cannot be
        # JSON serialized, it's safe to remove it
        for item in items:
            del item['published_parsed']
        kwargs.update({
            'feed_list': feeds, 'feed_count': len(feeds), 'item_list': items,
            'item_count': len(items)})
        return super(MixerView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        feed = parse(form.cleaned_data['url'])
        items = cache.get('items', {})
        items[slugify(feed.feed['title'])] = feed.entries
        cache.set('items', items)
        feeds = cache.get('feeds', {})
        feeds[slugify(feed.feed['title'])] = feed.feed.link
        cache.set('feeds', feeds)
        return super(MixerView, self).form_valid(form)


class DeleteView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        feeds = cache.get('feeds', {})
        feeds.pop(kwargs['feed'], None)
        cache.set('feeds', feeds)
        items = cache.get('items', {})
        items.pop(kwargs['feed'], None)
        cache.set('items', items)
        return super(DeleteView, self).get(request, *args, **kwargs)
