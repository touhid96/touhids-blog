from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
# posts = [
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 1',
#         'content': 'This is the first post of the blog',
#         'date_posted': 'March 22, 2021'
#     },

#     {
#         'author': 'John Smith',
#         'title': 'Blog Post 2',
#         'content': 'This is the second post of the blog',
#         'date_posted': 'March 23, 2021'
#     }

# ]


def home(request):

    context = {
        # 'posts': Posts
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # Validate form
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  # Validate form
        return super().form_valid(form)


# Prevent USERS from updating other users posts


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# Create your views here.
