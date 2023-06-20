from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from postsharing.forms import PostForm
from .models import Post, Comment, Like, Connection
from accounts.models import User


class ExploreView(ListView):
    model = Post
    template_name = 'posts/explore.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-modified_at')[:20]
    
class UserPage(DetailView):
    model = User
    template_name = 'posts/user_page.html'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/explore.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        following_set = set()
        following_set.add(user)
        for connection in user.friendship_creator_set.all():
            following_set.add(connection.following)

        return Post.objects.filter(user__in=following_set).order_by('-modified_at')
    
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/make_post.html'
    login_url = 'login'
    model = Post

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post.html'
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/edit_post.html'
    login_url = 'login'
    fields = ['title', 'picture', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/delete_post.html'
    login_url = 'login'
    success_url = reverse_lazy('posts')

def add_comment(request):
    if request.user.is_authenticated and request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.POST['post_id']
        content = request.POST['content']
        comment_info = {}
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        try:
            comment = Comment(post=post, content=content, user=user)
            comment.save()
            result = 1
            comment_info = {
                'user': user.username,
                'comment': comment.content,
            }
        except:
            result = 0

        return JsonResponse({
            'result': result,
            'post_id': post_id,
            'comment_info': comment_info,
        })


def add_like(request):
    if request.user.is_authenticated and request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        post_id = request.POST['post_id']
        post = get_object_or_404(Post, id=post_id)
        try: 
            like = Like(post=post, user=request.user)
            like.save()
            result = 1
        except:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            result = 0

        return JsonResponse({
            'result': result,
            'post_id': post_id,
        })
 
def toggle_follow_unfollow(request):
    if request.user.is_authenticated and request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_id = request.POST['user_id']
        type = request.POST['type']
        owner = get_object_or_404(User, id=user_id)

        try:
            if request.user != owner:
                if type == 'follow':
                    print('this is from follow')
                    connection = Connection(follower=request.user, following=owner)
                    connection.save()
                elif type == 'unfollow':
                    print('this is from unfollow')
                    connection = Connection.objects.get(follower=request.user, following=owner)
                    connection.delete()
                result = 1
            else: 
                result = 0
        except Exception as e:
            print(e)
            result = 0

        return JsonResponse({
            'result': result,
            'type': type,
            'user_id': user_id,
        })
