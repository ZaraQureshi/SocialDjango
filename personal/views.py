from django.shortcuts import render
from account.models import Account
from blog_api.models import BlogPost
from operator import attrgetter
from blog_api.views import get_blog_queryset
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

BLOG_POST_PER_PAGE=2

def home_screen(request):
    context={}
    #Searching
    query=""
    if request.GET:
        query=request.GET.get('q','')
        context['query']=str(query)
    blog_posts=sorted(get_blog_queryset(query),key=attrgetter('date_updated'),reverse=True)

    #Pagination
    page=request.GET.get('page',1)
    blog_posts_paginator=Paginator(blog_posts,BLOG_POST_PER_PAGE)
    try:
        blog_posts=blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts=blog_posts_paginator.page(BLOG_POST_PER_PAGE)
    except EmptyPage:
        blog_posts=blog_posts_paginator.page(blog_posts_paginator.num_pages)



    
    context['blog_posts']=blog_posts
    return render(request,'personal/home.html',context)