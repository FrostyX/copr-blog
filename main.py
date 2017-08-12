# -*- coding: utf-8 -*-

import time
import feedparser
from jinja2 import Environment, FileSystemLoader, select_autoescape



feeds = {
    "http://miroslav.suchy.cz/blog/archives/fedora/index-rss.xml" : {
        "title": "title", "url": "link", "author": "author", "date": "updated_parsed"
    },

    "http://frostyx.cz/fedora.xml": {
        "title": "title", "url": "link", "author": "Jakub Kadlcik", "date": "published_parsed"
    },
}



### Models/helpers/other
class Post(object):
    def __init__(self, title=None, url=None, perex=None, author=None, date=None):
        self.title = title
        self.url = url
        self.perex = perex
        self.author = author
        self.date = date

    @property
    def date_str(self):
        return time.strftime("%d. %b %Y", self.date)


def get_posts_from_feed(url, argmap):
    feed = feedparser.parse(url)
    posts = []
    for item in feed["items"]:
        post = Post()
        for key1, key2 in argmap.items():
            setattr(post, key1, item.get(key2, key2))
        posts.append(post)
    return posts



### Main
posts = []
for url, argmap in feeds.items():
    posts += get_posts_from_feed(url, argmap)
posts = sorted(posts, key=lambda post: post.date)
posts.reverse()



### Template rendering
env = Environment(
    loader=FileSystemLoader(searchpath="."),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html')

print(template.render(posts=posts).encode("utf-8"))
