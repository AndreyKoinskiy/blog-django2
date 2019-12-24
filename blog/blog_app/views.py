from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
# Create your views here.

def post_share(request,post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) recommends you reading  {post.title}'
            message = f'Read {post.title} at {post._url}\n\n{cd["name"]}\'s comments: {cd["comments"]}'
            sent = True
    else:
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post':post,'form':form,'sent':sent})



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list,3)# 3 articles per page
    page = request.GET.get('page') if request.GET.get('page') else 1
    posts = {}

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    print (page)
    print (posts)
    return render(request, 'blog/post/list.html', {'page':page,'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status = 'published', publish__year = year, publish__month = month, publish__day = day)
    comments = post.comments.filter(active = True)
    new_comment = None
    comment_form = None
    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post,'new_comment':new_comment, 'comment_form':comment_form, 'comments':comments})
