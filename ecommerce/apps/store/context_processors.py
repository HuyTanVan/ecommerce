from .models import Category
from .forms import PostSearchForm
def categories(request):

    return {
        'categories': Category.objects.all()
    }
def search_engine(request):
    form = PostSearchForm()
    return {'form': form}