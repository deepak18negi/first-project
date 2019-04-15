import json

from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import HttpResponse

from post.models import Post


def home(request):
    """
    Here taking the 5 posts in each page through paginator and 
    when the ajax request is received, each page will be assigned with variable posts and 
    each posts will be assigned with content variable which will be looped in index.html.
    """
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 5)
    if request.is_ajax():
        page = int(request.GET.get('page'))
        posts = paginator.get_page(page)
        content = render_to_string('post/index.html', {'posts': posts})
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
        return render(request, 'post/base.html', {'posts': posts})


def create_post(request):
    """
    When the user clicks the post button, with the contents in the textfield,
    input gets stored in the content variable and saved in the database.
    and send the response dictionary in JSON fromat.
    """
    response = {"status": False}
    content = request.POST.get('content')
    if content:
        post = Post()
        post.content = content
        post.save()
        response = {"status": True, "content": content}
    return HttpResponse(json.dumps(response),
                        content_type="application/json"
                        )
