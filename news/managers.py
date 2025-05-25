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
