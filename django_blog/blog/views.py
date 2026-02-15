from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PostForm, RegisterForm

from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post

from .models import Comment,Tag
from .forms import CommentForm
from django.db.models import Q  
# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()

    return render(request, 'blog/register.html', {'form': form})


# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.email = request.POST.get('email')
        request.user.save()
        return redirect('profile')

    return render(request, 'blog/profile.html')

# List view
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

# Detail view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

# Create view
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm   
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']   
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)


        tags_input = self.request.POST.get('tags', '')
        tag_list = tags_input.split(',')

        for tag_name in tag_list:
            tag_name = tag_name.strip()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag)

        return response


# updateing
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm 
    fields = ['title', 'content', 'tags']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        response = super().form_valid(form)

        # ✅ Clear old tags first
        self.object.tags.clear()

        # ✅ Add new tags
        tags_input = self.request.POST.get('tags', '')
        tag_list = tags_input.split(',')

        for tag_name in tag_list:
            tag_name = tag_name.strip()

            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag)

        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# delete view
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

def posts_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.posts.all()

    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag,
        'posts': posts
    })

def search_posts(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'blog/search_results.html', {
        'query': query,
        'results': results
    })
