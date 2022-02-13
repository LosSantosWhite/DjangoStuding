from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .models import Post
from .forms import CommentForm
from taggit.models import Tag

# class PostList(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 9
#     template_name = 'app_news/post/list.html'
#     tag = None
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PostList, self).get_context_data(**kwargs)
#         if self.kwargs['tag_slug']:
#             self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
#             self.queryset = Post.objects.filter(tags__in=[self.tag])
#             context['tag'] = self.tag
#         return context

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'app_news/post/list.html', context={
        'page':page, 'posts':posts, 'tag':tag
    })

class PostDetail(DetailView, FormView):
    model = Post
    template_name = 'app_news/post/detail.html'
    form_class = CommentForm
    new_comment = None

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['post'] = self.object
        context['comments'] = self.object.comments.filter(active=True)
        context['new_comment'] = self.new_comment
        if self.request.user.is_authenticated:
            self.form_class = CommentForm(hidden=True)
            context['form'] = self.form_class

        return context

    def form_valid(self, form):
        self.object = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.post = self.object
        if not self.request.user.is_authenticated:
            new_comment.name += " Аноним"
            new_comment.user_id = None
        else:
            new_comment.name = self.request.user
        new_comment.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.user.is_authenticated:
            form = CommentForm(hidden=True)
        else:
            form = CommentForm()
        return super().form_invalid(form)

    def get_success_url(self):
        return self.request.path


    def get_object(self, queryset=None, **kwargs):
        return Post.objects.get(id=self.kwargs['pk'])


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'bode', 'author', 'status']
    template_name = 'app_news/post_create.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'bode', 'author', 'status']
    template_name = 'app_news/post_create.html'
