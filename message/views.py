from django.shortcuts import render
from .models import Comment, CommentManager
from .forms import NewComment
from command.views import OrderManager, StaffManager
# Create your views here.

def new_comment(request):
    user = request.user
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            check = Comment.objects.filter(user=user, message=message)
            if not check:
                CommentManager().new_comment(user=user, message=message)
            
    return OrderManager().ordering(request)

def check_comment(request):
    
    if request.GET.get('change'):
        message_id = int(request.GET.get('change'))
    
        CommentManager().change_visibility(message_id=message_id)
        return StaffManager().all_data(request)