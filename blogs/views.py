from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.db.models import Q

from blogs.models import Post, Category

# Create your views here.

def home_page(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True)[:3]

    context = {
        'post_list' : posts,
        'categories' : categories,
        'featured' : featured,
    }

    return render(request, 'blogs/home_page.html', context=context)

class PostDetailView(generic.DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class FeaturedListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = Post.objects.filter(featured=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class CategoryListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = self.request.path.replace('/category/', '')
        print(query)
        post_list = Post.objects.filter(categories__slug=query)
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
