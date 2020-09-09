from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from allauth import User

# Create your models here.



class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)#models.CharField(max_length=200, null=False)
    message = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return (str(self.user)+'--'+str(self.date))

class CommentManager(models.Model):

    def new_comment(self, user, message):
        new_entry = Comment.objects.create(
            user=user,
            message=message,
        )
        new_entry.save()
    
    def change_visibility(self, message_id):

        to_change = Comment.objects.get(pk=message_id)
        if to_change.visible:
            to_change.visible = False
        else:
            to_change.visible = True
        to_change.save()
