import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import HttpResponse

from post.models import Post
from post.forms import PostForm


@login_required
def home(request):
    """
    Here taking the 5 posts in each page through paginator and 
    when the ajax request is received, each page will be assigned with variable posts and 
    each posts will be assigned with content variable which will be looped in index.html.
    """
    p_form = PostForm(request.POST, request.FILES)
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 5)
    if request.is_ajax():
        page = int(request.GET.get('page'))
        posts = paginator.get_page(page)
        content = render_to_string('post/cont.html', {'posts': posts})
        response = {
            'content': content,
            'next_page': str(page + 1),
            'has_next': posts.has_next()
        }
        return HttpResponse(json.dumps(response),
                            content_type="application/json"
                            )
    else:
        posts = paginator.get_page(1)
        p_form = PostForm()
        return render(request, 'post/index.html', {'posts': posts, 'p_form': p_form})


@login_required
def create_post(request):
    if request.method == 'POST':
        response = {"status": False}
        p_form = PostForm(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            posts = Post.objects.order_by('-pub_date')[:1]
            context = render_to_string('post/cont.html', {'posts': posts})
            response = {"status": True,
                        "context": context}
            return HttpResponse(json.dumps(response),
                                content_type="aplication/json")
