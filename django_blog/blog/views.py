from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserUpdateForm, PostForm, CommentForm
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.urls import reverse_lazy , reverse 
from django.db.models import Q 


def home(request):
    return render(request, 'blog/base.html')

def post_list(request):
    return HttpResponse("post list page")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect('login')
        
    else:
        form = UserCreationForm()

    return render(request, 'blog/register.html', {'form':form})       

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfuly!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)    

    return render(request, 'blog/profile.html', {'form': form})    

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


# View single post
class PostListView(ListView):
    model = Post 
    template_name = 'blog/post_list.html'
    context_object_name = 'post' 
    ordering = ['-published_date']


    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        if tag_name:
            return Post.objects.filter(tags__name__iexact=tag_name)
        return Post.objects.all().order_by('-published_date')

# View single post

class PostDetailView(DetailView):
    model = Post 
    template_name = 'blog/post_detail.html' 
    context_object_name = 'post' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

# Create a post
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm  
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form) 
    
# update a post    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post 
    form_class = PostForm 
    template_name = 'blog/post_form.html' 

    def test_func(self):
        post = self.get_object() 
        return self.request.user == post.author 
    
# Delete a post 
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    template_name = 'blog/post_confirm_delete.html' 
    success_url = reverse_lazy('posts') 

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author     



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm 
    template_name = 'blog/comment_form.html' 

    def test_func(self):
        comment = self.get_object() 
        return self.request.user == comment.author 
    
    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment 
    template_name = 'blog/comment_confirm_delete.html' 

    def test_func(self):
        comment = self.get_object() 
        return self.request.user == comment.author 

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})    
    
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html' 
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags_name=self.kwargs['tag_name'])
    
class SearchResultsView(ListView):
    model = Post 
    template_name = 'blog/search_results.html' 
    context_object_name = 'posts' 

    def get_queryset(self):
        query = self.request.Get.get('q') 
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none() 

def search_posts(request):
    query = request.GET.get('q') 
    posts = Post.objects.none() 
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
         
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})    


    


