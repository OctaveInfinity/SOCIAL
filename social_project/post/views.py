from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)

from .models import Post




class PostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html 
    template_name = 'post/post_list.html'
    context_object_name = 'posts'
    ordering = ['-posted']
    paginate_by = 4



class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts.html' 
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(owner=user).order_by('-posted')



class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        user = self.request.user
        like_button = "Like"
        if user in post.liked.all():
            like_button = "Unlike"
        context["like_button"] = like_button
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/social/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False



class PostLikeToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        user = self.request.user
        if user in post.liked.all():
            post.liked.remove(user)
        else:
            post.liked.add(user)
        return post.get_absolute_url()
