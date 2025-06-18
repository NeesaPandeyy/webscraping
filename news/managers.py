from django.db import models


class LikeManager(models.Manager):
    def toggle_like(self, user, post):
        like = self.filter(user=user, post=post).first()
        if like:
            like.delete()
            return False
        else:
            self.create(user=user, post=post)
            return True


class BookmarkManager(models.Manager):
    def toggle_bookmark(self, user, post):
        bookmark = self.filter(user=user, post=post).first()
        if bookmark:
            bookmark.delete()
            return False
        else:
            self.create(user=user, post=post)
            return True
