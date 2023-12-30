from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from leapcell import Leapcell
import os
import markdown
import datetime
import time
from dotenv import load_dotenv
import os
from django.template import loader
load_dotenv()

api = Leapcell(
    os.environ.get("LEAPCELL_API_KEY"),
)

author = os.environ.get("AUTHOR", "Leapcell User")
avatar = os.environ.get("AVATAR", "https://leapcell.io/logo.png")
resource = os.environ.get("TABLE_RESOURCE", "issac/flask-blog")
table_id = os.environ.get("TABLE_ID", "tbl1738878922167070720")

table = api.table(repository=resource, table_id=table_id)


def index(request):
    records = table.select().query()
    items = []
    for record in records:
        item = record.data()
        item["id"] = record.id

        item["create_time"] = datetime.datetime.fromtimestamp(record.create_time).strftime("%B %d, %Y %H:%M:%S")
        item["summary"] = item["content"][:200]
        items.append(item)
    params = {
        "author": author,
        "avatar": avatar,
        "posts": items,
        "category": None,
        "query": None,
    }

    return render(request, "blog/index.html", params)


def category(request, category):
    records = table.select().where(table["category"].contain(category)).query()
    items = []
    for record in records:
        item = record.data()
        item["id"] = record.id

        item["create_time"] = datetime.datetime.fromtimestamp(record.create_time).strftime("%B %d, %Y %H:%M:%S")
        item["summary"] = item["content"][:200]
        items.append(item)
    params = {
        "author": author,
        "avatar": avatar,
        "posts": items,
        "category": category,
        "query": None,
    }
    return render(request, "blog/index.html", params)


def search(request):
    query = request.GET.get("query", "")
    records = table.search(query=query)
    items = []
    for record in records:
        item = record.data()
        item["id"] = record.id

        item["create_time"] = datetime.datetime.fromtimestamp(record.create_time).strftime("%B %d, %Y %H:%M:%S")
        item["summary"] = item["content"][:200]
        items.append(item)
    params = {
        "author": author,
        "avatar": avatar,
        "posts": items,
        "category": None,
        "query": query,
    }
    return render(request, "blog/index.html", params)


def post(request, post_id):
    record = table.get_by_id(post_id)
    markdown_html = markdown.markdown(record["content"])
    item = record.data()
    params = {
        "author": author,
        "avatar": avatar,
        "post": item,
        "markdown_html": markdown_html,
        "create_time": datetime.datetime.fromtimestamp(record.create_time).strftime("%B %d, %Y %H:%M:%S"),
    }
    return render(request, "blog/post.html", params)