from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Article, CartItem, Comment, Product
from .forms import ArticleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils import timezone
from .forms import ProductForm

# Create your views here.
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles": articles})

    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="user:login")
def addArticle(request):
    # Supervisor veya Admin kontrolü
    if not request.user.groups.filter(name="supervisors").exists() and not request.user.is_superuser:
        messages.error(request, "Bu işlemi gerçekleştirmek için yetkiniz yok.")
        return redirect("article:dashboard")

    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Ürün Başarıyla Oluşturuldu.")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form": form})

def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request, "detail.html", {"article": article, "comments": comments})

@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Ürün Başarıyla Güncellendi.")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Ürün başarıyla silindi")

    return redirect("article:dashboard")
@login_required(login_url="user:login")
def addComment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        if comment_author and comment_content:
            newComment = Comment(
                article=article,
                comment_author=comment_author,
                comment_content=comment_content,
            )
            newComment.save()
        else:
            return redirect(f"/articles/article/{id}?error=missing_fields")

    return redirect(f"/articles/article/{id}")

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Burada form verilerini işleyin ve ürünü kaydedin
            # Örneğin: Product.objects.create(**form.cleaned_data)
            return redirect('success_url')  # Başarılı yönlendirme
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    
