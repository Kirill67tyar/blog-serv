from django.conf import settings
from django.db.models import Count
from django.core.mail import send_mail
from django.views.generic import ListView
from django.shortcuts import (
    render, get_object_or_404,
    redirect, reverse, HttpResponse,
)
from django.core.paginator import (
    Paginator, PageNotAnInteger, EmptyPage,
)

from blog.models import Post, Tag
from blog.forms import EmailForm, CommentModelForm
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
    comments = post.comments.filter(active=True).select_related('author')
    new_comment = None
    user = request.user
    tag_ids = post.tags.values_list('pk', flat=True)
    similar_posts = Post.published.filter(tags__in=tag_ids).exclude(pk=post.pk)
    similar_posts = similar_posts.annotate(quantity_tags=Count('tags')).order_by('-quantity_tags', '-publish')[:4]
    ctx = {
        'object': post,
        'comments': comments,
        'author': user,
        'similar_posts': similar_posts,
    }
    if request.method == 'POST':
        if user.is_authenticated:
            form = CommentModelForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = user
                new_comment.save()
            else:
                ctx['form'] = form
                ctx['new_comment'] = new_comment
                return render(request, 'blog/detail.html', context=ctx)
        else:
            return HttpResponse(
                '<h1>Сначала нужно зарегистрироваться, или авторизоваться, а таких обработчиков у нас нет:)</h1>')
    ctx['form'] = CommentModelForm()
    ctx['new_comment'] = new_comment
    return render(request, 'blog/detail.html', context=ctx)


def post_list_view(request, slug_tag=None):
    post_list = Post.published.all().prefetch_related('tags')
    tag = None
    if slug_tag:
        tag = get_object_or_404(Tag, slug=slug_tag)
        post_list = post_list.filter(tags__in=[tag])
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
        'tag': tag,
    }
    return render(request=request,
                  template_name='blog/list.html',
                  context=context_)


class PostListView(ListView):
    # model = Post # будет доставать QS - Post.objects.all()
    queryset = Post.published.all().prefetch_related('tags')
    paginate_by = 2
    template_name = 'blog/list.html'

    # функция для определения тега (если есть тег, то она его возвращает)
    # очень много костылей здесь
    def tag_in_path(self):
        url_path = self.request.path_info.strip('/').split('/')
        if 'tag' in url_path and len(url_path):
            slug_tag = url_path[-1]
            return get_object_or_404(Tag, slug=slug_tag)

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.tag_in_path()
        if tag:
            return qs.filter(tags__in=[tag]).prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        tag = self.tag_in_path()
        if tag:
            ctx['tag'] = tag
        return ctx

    # # а здесь ничего не поменяется, т.к. ListView при атрибуте paginate_by
    # # будет выводить в контекст page_obj (без paginate_by по умолчанию object_list )
    # context_object_name = 'posts'


def post_share_view(request, post_id):
    # if request.user.is_authenticated:
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
    # else:
    #     return redirect
