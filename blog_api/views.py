from django.shortcuts import render,redirect,get_object_or_404
from blog_api.forms import CreateBlogPost,UpdateBlogPost
from account.models import Account
from blog_api.models import BlogPost
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
def create_blog_view(request):
    context={}
    user=request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form=CreateBlogPost(request.POST or None ,request.FILES or None)
    if form.is_valid():
        obj=form.save(commit=False)
        author=Account.objects.filter(email=user.email).first()
        obj.author=author
        obj.save()
        form=CreateBlogPost()

    context['from']=form
    return render(request,'blog_api/create_blog.html',{})


def detail_blog_view(request,slug):
    context={}
    blog_post=get_object_or_404(BlogPost,slug=slug)
    context['blog_post']=blog_post

    return render(request,'blog_api/detail_blog_view.html',context)

def update_blog_view(request,slug):
    context={}
    user=request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')
    
    blog_post=get_object_or_404(BlogPost,slug=slug)
    
    #authentication for non owners trying to edit
    if blog_post.author != user:
        return HttpResponse('You are not the owner of this blog')
    if request.POST:
        form=UpdateBlogPost(request.POST or None ,request.FILES or None,instance=blog_post)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            context['success_message']='Updated'
            blog_post=obj
    form=UpdateBlogPost(
        initial={
            'title':blog_post.title,
            'body':blog_post.body,
            'image':blog_post.image,
        }

    )
    context['form']=form
    return render(request,'blog_api/update_blog.html',context)


# search
def get_blog_queryset(query=None):
    queryset=[]
    queries=query.split(" ")
    for q in queries:
        posts=BlogPost.objects.filter(
            Q(title__icontains=q)|
            Q(body__icontains=q)|
            Q(author__username__icontains=q)
            
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset)) 
