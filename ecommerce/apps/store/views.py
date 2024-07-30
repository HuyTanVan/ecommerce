from django.shortcuts import render, get_object_or_404
from .models import (Category, Product, Inventory)
from .forms import PostSearchForm
# Create your views here.

def categories(request):
    return {'categories': Category.objects.all()}
def search_engine(request):
    # 1.0.1 Standard textual queries (case sensitive)
      # results = Book.objects.filter(title__contains=q)
      # print(Book.objects.filter(title__contains=q).explain(verbose=True, analyze=True))
      # print(Book.objects.filter(title__contains=q).query)

    # # 1.0.2 Standard textual queries (case insensitive)      
      # results = Book.objects.filter(title__icontains=q)
        
    # 1.0.3 Full text search
      # results = Book.objects.filter(title__search=q)

    # 1.0.4 SearchVector (search against multiple fields)
      # from django.contrib.postgres.search import SearchVector
      # results = Book.objects.annotate(search=SearchVector('title', 'authors'),).filter(search=q)  

    # 1.0.5 Search Ranking
      # from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
      # vector = SearchVector('title', weight='A') + SearchVector('authors', weight='B')
      # query = SearchQuery(q)
      # results = Book.objects.annotate(rank=SearchRank(vector, query, cover_density=True)).order_by('-rank')

    # 1.0.6 Search TrigramSimilarity & TrigramDistance
      # from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
      # results = Book.objects.annotate(similarity=TrigramSimilarity('title', q),).filter(similarity__gte=0.3).order_by('-similarity')
      # results = Book.objects.annotate(distance=TrigramDistance('title', q),).filter(distance__lte=0.8).order_by('distance')

    # 1.0.7 Search Headline
      # from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchVector
      # query = SearchQuery(q)
      # vector = SearchVector('authors')
      # results = Book.objects.annotate(search=vector, headline=SearchHeadline('authors', query, start_sel='<span>', stop_sel='</span>', )).filter(search=query)
    form = PostSearchForm
    # results = []
    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            results = Product.objects.filter(name__contains=q)
    print("HERE IS RESULT: ", results)
    return render(request, 'store/search_results.html', {'form': form, 'results': results})
def all_products(request): # return in homepage
    inventories = Inventory.objects.all()
    return render(request, 'store/home.html', {'inventories': inventories})
def product_detail(request, slug, sku):
    # product = get_object_or_404(Inventory, slug=slug)
    product = Product.objects.get(slug=slug)
    inventory = Inventory.objects.get(sku=sku)
    # product = Inventory.objects.filter(product=product)
    return render(request, 'store/products/detail.html', {'product': product, 'inventory': inventory})
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


