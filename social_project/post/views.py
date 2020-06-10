from django.shortcuts import render



posts = [
    {
        'owner'     : 'Emako',
        'title'     : 'Title Post_1',
        'content'   : 'Content Post1 ............. .',
        'posted'    : 'April 27, 2020',
    },
    {
        'owner'     : 'Other',
        'title'     : 'Title Post_2',
        'content'   : 'Content Post_2 ............. .',
        'posted'    : 'April 27, 2020',
    },
]

def PostList(request):
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)
