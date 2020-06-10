from django.shortcuts import render

from .models import Post



def PostList(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'post/post_list.html', context)
