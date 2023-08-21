from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserSignupForm, BlogForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Blog, Category
from user_auth.decorators import patient_required, doctor_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# utility functions


def check_confirm_password(form):
    if form.cleaned_data['password'] != form.cleaned_data['password_confirm']:
        return True
    return False


def redirect_to_dashboard(user):
    if user.profile_type == 'Patient' or user.profile_type == 'patient':
        return 'patient_dashboard'
    elif user.profile_type == 'Doctor' or user.profile_type == 'doctor':
        return 'doctor_dashboard'

# all the urls


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = Blog.objects.filter(
        (Q(author=request.user) | Q(draft=False))
    )
    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)

    categorys = Category.objects.all()
    context = {'blogs': blogs,
               'categorys': categorys,
               'page_obj': page_obj}
    return render(request, 'user_auth/index.html', context)


@login_required(login_url='login')
def category(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    blogs = Blog.objects.filter(
        Q(category__name=q) &
        (Q(author=request.user) | Q(draft=False))
    )

    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)
    categorys = Category.objects.all()
    context = {'blogs': blogs, 'categorys': categorys,
               'page_obj': page_obj, 'q': q}
    return render(request, 'user_auth/Category.html', context)


@doctor_required
def self_blogs(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(author__username__icontains=request.user)
    )
    p = Paginator(blogs, 4)

    page_number = request.GET.get(
        'page') if request.GET.get('page') != None else '1'
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_number = '1'
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_number = p.num_pages
        page_obj = p.page(p.num_pages)

    categorys = Category.objects.all()
    context = {'blogs': blogs, 'categorys': categorys,
               'page_obj': page_obj, 'q': q}
    return render(request, 'user_auth/self_blog.html', context)


def signup(request):

    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)

            # checking if the pass is same as confirm_pass
            if check_confirm_password(form):
                return render(request, 'user_auth/signup.html', {'form': form})

            password = form.cleaned_data['password']
            username = form.cleaned_data['username']

            user.set_password(password)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('login')
        else:
            print(form.errors)
    else:

        form = UserSignupForm()
    return render(request, 'user_auth/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        dashboard_url = redirect_to_dashboard(request.user)
        return redirect(dashboard_url)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(request.user.profile_picture,
                  type(request.user.profile_picture))
            return redirect('home')
    return render(request, 'user_auth/login.html')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@patient_required
def patient_dashboard(request):
    user = request.user
    return render(request, 'user_auth/patient_dashboard.html', {'user': user})


@doctor_required
def doctor_dashboard(request):
    user = request.user
    return render(request, 'user_auth/doctor_dashboard.html', {'user': user})


def blog_detail(request, slug):
    blog = Blog.objects.get(pk=slug)

    context = {'blog': blog}
    return render(request, 'user_auth/blog.html', context)


@doctor_required
def create_blog(request):
    page = 'create'
    if request.method == 'POST':
        blog_category = request.POST.get('category')
        cate_old, created = Category.objects.get_or_create(name=blog_category)

        # Creating a new Blog instance
        blog = Blog.objects.create(
            author=request.user,
            name=request.POST.get('name'),
            category=cate_old,
            content=request.POST.get('content'),
            draft=request.POST.get('draft') == 'on'
        )

        # Handling blog_picture upload separately
        blog.blog_picture = request.FILES.get('blog_picture')
        blog.save()
        return redirect('blog_detail', slug=blog.id)
    else:
        form = BlogForm()
    categorys = Category.objects.all()  
    context = {'form': form, 'categorys': categorys, 'page': page}
    return render(request, 'user_auth/create_blog.html', context)


@doctor_required
def update_blog(request, slug):
    page = 'update'
    blog = Blog.objects.get(pk=slug)

    if request.user != blog.author:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        blog_category = request.POST.get('category')
        cate_old, created = Category.objects.get_or_create(name=blog_category)
        blog.name = request.POST.get('name')
        blog.category = cate_old
        blog.content = request.POST.get('content')
        blog.draft = request.POST.get('draft') == 'on'
        if request.FILES.get('blog_picture'):
            blog.blog_picture = request.FILES.get('blog_picture')
        blog.save()
        return redirect('blog_detail', slug=blog.id)
    else:
        form = BlogForm(instance=blog)

    categorys = Category.objects.all()
    context = {'form': form, 'blog': blog,
               'categorys': categorys, 'page': page}
    return render(request, 'user_auth/create_blog.html', context)
