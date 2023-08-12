from django.shortcuts import render
from django.http import HttpResponse
from blogs.models import Post, Category

# Create your views here.

def home_page(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    context = {
        'posts' : posts,
        'categories' : categories,
    }
    return render(request, 'blogs/home_page.html', context=context)