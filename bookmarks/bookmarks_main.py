# coding: utf-8
import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from datetime import datetime

from google.appengine.ext import db, webapp

class Bookmark(db.Model):
    title= db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    comment = db.TextProperty()
class MainPage(webapp.RequestHandler):
    def get(self):
        today=datetime.strftime(datetime.now(), "%Y/%m/%d")
        data={"today": today}
        path = os.path.join(os.path.dirname(__file__), "bookmarks_home.html")
        self.response.out.write(template.render(path, data))

class ListBookmark(webapp.RequestHandler):
    def get(self):
        bookmarks = Bookmark.all()
        data = {"bookmarks": bookmarks}
        path = os.path.join(os.path.dirname(__file__),
                            "bookmark_list.html")
        self.response.out.write(template.render(path,data))

def main():
    application=webapp.WSGIApplication([("/", ListBookmark),
                                        ("/add/", AddBookmark),
                                        ("/edit/(\d+)", EditBookmark),
                                        ("/delete/(\d+)", DeleteBookmark),
                                        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

class AddBookmark(webapp.RequestHandler):
    def get(self):
        """新規登録画面を表示する
        """
        bookmarks = Bookmark.all()
        data = {"bookmarks": bookmarks}
        path = os.path.join(os.path.dirname(__file__), "bookmark_add.html")
        self.response.out.write(template.render(path, data))

    def post(self):
        """新規登録処理を行い、編集画面に遷移する。
        """
        url = self.request.POST["url"]
        title = self.request.POST["title"]
        bookmark = Bookmark(url=url, title=title)
        bookmark.comment = self.request.POST["comment"]
        bookmark.put()
        self.redirect("/edit/%d/" % (bookmark.key().id()))

class EditBookmark():
    pass

class DeleteBookmark():
    pass

if __name__=="__main__":
    main()
