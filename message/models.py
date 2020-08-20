from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from allauth import User

# Create your models here.

"""class CommentManager(models.Model):

    def new_comment(self, data):
        new_entry = Comment.objects.create(
            user=data.user,
            message=data.message,
        )
        new_entry.save()
    
    def new_answer(self, data):
        new_entry = Comment.objects.create(
            user=data.user,
            message=data.message,
        )
        new_entry.save()"""

class Comment(models.Model):

    #post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)#models.CharField(max_length=200, null=False)
    #staff = models.BooleanField(default=False)
    ##number = models.IntegerField(null=False, default=1)
    message = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return (str(self.user)+'--'+str(self.date))


"""class Conversation(models.Model):

    reference = models.ForeignKey(Comment, on_delete=models.CASCADE)
    answer = models.IntegerField(null=False)"""