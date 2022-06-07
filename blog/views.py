from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import (
    Paginator, PageNotAnInteger, EmptyPage,
)

from blog.models import Post
from blog.forms import EmailForm
from blog.utils import get_object_or_null

# ---------------------------------- analizetools
from blog.utils import (
    p_dir, p_mro,
    p_glob, p_loc, p_type,
    p_content, show_doc,
    delimiter, show_builtins, console
)


#     'p_dir', 'p_mro',
#     'p_glob', 'p_loc', 'p_type',
#     'p_content', 'show_doc',
#     'delimiter', 'show_builtins', console
# ---------------------------------- analizetools


def post_detail_view(request, year, month, day, post):
    params = {
        'klass': Post,
        'publish__year': year,
        'publish__month': month,
        'publish__day': day,
        'slug': post,
    }
    post = get_object_or_404(**params)
    # post = get_object_or_null(**params)
    return render(request, 'blog/detail.html', {'object': post, })


def post_list_view(request):
    post_list = Post.published.all()
    paginator_ = Paginator(object_list=post_list, per_page=2)
    num_page = request.GET.get('page')
    try:
        page_obj = paginator_.page(num_page)
    except PageNotAnInteger:
        page_obj = paginator_.page(1)
    except EmptyPage:
        page_obj = paginator_.page(paginator_.num_pages)
    context_ = {
        'page_obj': page_obj,
        'page': num_page,
    }
    return render(request=request,
                  template_name='blog/list.html',
                  context=context_)


class PostListView(ListView):
    # model = Post # будет доставать QS - Post.objects.all()
    queryset = Post.published.all()
    paginate_by = 2
    template_name = 'blog/list.html'

    # # а здесь ничего не поменяется, т.к. ListView при атрибуте paginate_by
    # # будет выводить в контекст page_obj (без paginate_by по умолчанию object_list )
    # context_object_name = 'posts'


def post_share_view(request, post_id):
    post = get_object_or_404(klass=Post, pk=post_id, status='publish')
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # --- in console ---
            for_console = [
                post.get_absolute_url(),
                post_url,
                request.path,
                request.path_info,
                request.get_host(),
                request.get_full_path_info(),
                request.get_full_path(),
            ]
            console(*for_console, delimetr='- ')  # --- in console
            # --- in console ---
            
            subject = f'{cd["name"]} ({cd["email"]}) recommends you reading {post}'
            message = f'Read {post} at {post_url} \n\n comments: {cd["comment"]}'
            params = {
                'subject': subject,
                'message': message,
                'from_email': settings.EMAIL_HOST_USER,
                'recipient_list': [cd['to'], ],
            }
            send_mail(**params)
            sent = True
    else:
        form = EmailForm()
    ctx = {
        'form': form,
        'sent': sent,
        'post': post,
    }
    return render(request, 'blog/send_email.html', context=ctx)

