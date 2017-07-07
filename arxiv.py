# coding=utf-8
"""
    arXiv.py -- sopel arXiv Module

    Copyright 2017 Sujeet Akula (sujeet@freeboson.org)
    MIT License

"""

from sopel import tools, web
from sopel.module import rule, commands, example
import re, feedparser
import sys
import requests

arxiv_catch = re.compile(
    r"""
        (http[s]?://[^/]*xxx\.lanl\.gov/[a-z]+/|    # old domain
         http[s]?://[^/]*arxiv\.org/[a-z]+/|        # main
         arxiv:)                                    # common shorthand
        (                                           # arXiv id in group(2)
            \d{4}\.\d{4,5}                          # new and newer fmts
        |
            [\w\-\.]+/\d{7}                         # old format
        )
    """, re.X)

# Base api query url
base_url = 'https://export.arxiv.org/api/query'

feedparser._FeedParserMixin.namespaces['https://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['https://arxiv.org/schemas/atom'] = 'arxiv'

id_filter = re.compile(
    r"""
        .*\/abs\/                                   # gives abs link
        (                                           # arXiv id in \1
            \d{4}\.\d{4,5}                          # new and newer fmts
        |
            [\w\-\.]+/\d{7}                         # old format
        )
        (v\d+){,1}                                  # get rid of version
        [/]{,1}                                     # "   "   "  trailing slash
    """, re.X)

collab_check = re.compile(r'\s(?:Collaboration)|(?:Group).*', flags=re.IGNORECASE)

no_newlines = re.compile(r'\n')
http = re.compile(r'http:')

def httpsify(url):
    http.sub('https:', url)

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][arxiv_catch] = info

def shutdown(bot):
    del bot.memory['url_callbacks'][arxiv_catch]

def get_arxiv(query):

    request = {
        'start' : 0,
        'max_results' : 1,
        'search_query' : query
    }

    xml = requests.get(base_url,
                params=request,
                timeout=40,
                headers=web.default_headers).text

    feed = feedparser.parse(xml)

    if int(feed.feed.opensearch_totalresults) < 1:
        raise IndexError

    # get the first (and only) entry
    entry = feed.entries[0]

    abs_link = entry.id
    arxivid = id_filter.sub(r'\1', abs_link)

    # format the author string
    # use et al. for 3+ authors
    if len(entry.authors) > 2:
        authors = entry.authors[0].name

        if collab_check.match(authors) is None:
            authors += ' et al.'

    elif len(entry.authors) >0:
        authors = ' and '.join([author.name for author in entry.authors])
    else:
        authors = ''

    title = entry.title
    abstract = no_newlines.sub(' ', entry.summary)

    return (arxivid, authors, title, abstract, httpsify(abs_link))

@commands('arxiv')
@example('.arxiv 1304.5526')
def print_summary(bot, input=None, arxiv_id=None, include_link=True):

    if arxiv_id is not None:
        query = 'id:' + arxiv_id
    else:
        query = input.group(2)

    if not query:
        return bot.say('[arXiv] Please provide an input to lookup.')

    try:
        (arxiv_id, authors, title, abstract, url) = get_arxiv(query)
    except:
        return bot.say("[arXiv] Could not lookup " + query + " in the arXiv.")

    if include_link:
        arxiv_summary = "[arXiv] " + authors + ', "' \
                        + title + '" :: ' + abstract

        long_summary = arxiv_summary + " " + url
        if len(long_summary) > 300:
            ending = '[…] ' + url
            clipped = arxiv_summary[:(300-len(ending))] + ending
        else:
            clipped = long_summary
    else:
        arxiv_summary = "[arXiv:" + arxiv_id + "] " + authors + ', "' \
                        + title + '" :: ' + abstract

        if len(arxiv_summary) > 300:
            ending = '[…]'
            clipped = arxiv_summary[:(300-len(ending))] + ending
        else:
            clipped = arxiv_summary

    bot.say(clipped)

@rule('.*(arxiv:|xxx\.lanl\.gov\/[a-z]+\/|arxiv\.org\/[a-z]+\/)(\d{4}\.\d{4,5}|[a-z\-\.]+/\d{7}).*')
def info(bot, trigger, found_match=None):
    match = found_match or trigger
    print_summary(bot, arxiv_id=match.group(2), include_link=False)


