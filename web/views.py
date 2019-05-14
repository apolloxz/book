from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from functools import wraps
from web import models
from web.get_md5 import get_md5


def check_form(*args):
    '''
    验证传入字段是否为空
    :param args: 需要校验的字段
    :return: 都不为空返回True，否则Fase
    '''
    for form in args:
        if not form:
            return False
    return True


def login(request):
    '''
    登录
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    pwd = get_md5(pwd)
    msg = {"error": None}
    userinfo = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if userinfo:
        request.session['userinfo'] = user
        msg['user'] = user
    msg['error'] = '密码和用户名不匹配'
    return JsonResponse(msg)


def login_check(func):
    # 装饰器，验证是否登录
    @wraps(func)
    def inner(request, *args, **kwargs):
        if request.session.get('userinfo'):
            ret = func(request, *args, **kwargs)
            return ret
        return login(request)

    return inner


@login_check
def index(request):
    '''
    首页,登录后才能看到
    :param request:
    :return:
    '''
    userinfo = request.session.get('userinfo')
    if not userinfo:
        return render(request, 'login.html')
    book_list = models.Book.objects.all()
    return render(request, 'index.html', {'book_list': book_list})


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'register.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    confirm_pwd = request.POST.get('confirm_pwd')
    msg = {"error": None}
    if pwd == confirm_pwd:
        userinfo = models.UserInfo.objects.filter(name=user).filter()
        if not userinfo:
            pwd = get_md5(pwd)
            models.UserInfo.objects.create(name=user, password=pwd)
            return redirect('/login/')
        msg['error'] = '用户名已存在'
    else:
        msg['error'] = "两次密码不一致"
    return render(request, 'register.html', msg)


def logout(request):
    '''
    注销登录
    :param request:
    :return:
    '''
    request.session.flush()
    return render(request, 'login.html')


@login_check
def book_add(request):
    '''
    添加书籍
    :param request:
    :return:
    '''
    publish_list = models.Publish.objects.all()
    author_list = models.Author.objects.all()
    if request.method == 'POST':
        date = request.POST
        title = date.get('title')
        price = date.get('price')
        publish_date = date.get('publish_date')
        publish = date.get('publish')
        author = date.getlist('author')
        if check_form(title, price, publish_date, publish, author):
            book_exist = models.Book.objects.filter(title=title).exists()
            if book_exist:
                return HttpResponse('该书已存在')
            book_object = models.Book.objects.create(title=title, publishDate=publish_date, price=price,
                                                     publish_id=publish)
            book_object.authors.add(*author)
            return redirect('/index/')
        return HttpResponse('请将信息填写完整')

    return render(request, 'book_add.html', {'publish_list': publish_list, 'author_list': author_list})


@login_check
def publish_add(request):
    '''
    添加出版社
    :param request:
    :return:
    '''
    if request.method == 'POST':
        date = request.POST
        title = date.get('title')
        city = date.get('city')
        email = date.get('email')
        if check_form(title, city, email):
            models.Publish.objects.create(name=title, city=city, email=email)
            return redirect('/index/')
        return HttpResponse('请将信息填写完整')

    return render(request, 'publish_add.html')


@login_check
def author_add(request):
    '''
    添加书籍
    :param request:
    :return:
    '''
    if request.method == 'POST':
        date = request.POST
        name = date.get('name')
        age = date.get('age')
        if check_form(name, age):
            models.Author.objects.create(name=name, age=age)
            return redirect('/index/')
        return HttpResponse('请将信息填写完整')

    return render(request, 'author_add.html')


@login_check
def book_edit(request, pk):
    '''
    编辑书籍
    :param request:
    :param pk:要编辑书籍的id
    :return:
    '''
    book_object = models.Book.objects.filter(pk=pk).first()
    publish_list = models.Publish.objects.all()
    authors_choice_object_list = book_object.authors.all()
    authors_list = models.Author.objects.all()

    if request.method == 'POST':
        msg = {'error': '请将信息填写完整'}
        date = request.POST
        title = date.get('title')
        price = date.get('price')
        publish_date = date.get('publish_date')
        publish = date.get('publish')
        author = date.getlist('author')[0].split(',')
        if check_form(title, price, publish_date, publish, author):
            models.Book.objects.filter(pk=pk).update(title=title, publishDate=publish_date, price=price,
                                                     publish_id=publish)
            book_object.authors.set(author)
            msg['error'] = None
        return JsonResponse(msg)

    return render(request, 'book_edit.html',
                  {'book': book_object, 'authors_list': authors_list, 'publish_list': publish_list,
                   'authors_choice_object_list': authors_choice_object_list})


@login_check
def book_del(request, pk):
    '''
    删除书籍
    :param request:
    :param pk:要删除书籍的ID
    :return:
    '''
    models.Book.objects.filter(pk=pk).first().delete()

    return redirect('/index/')


@login_check
def publish_book_list(request, pk):
    '''
    展示某个出版社，出版的书籍
    :param request:
    :param pk:要展示出版社的ID
    :return:
    '''
    book_list = models.Publish(pk=pk).book_set.all()
    return render(request, 'publish_book_list.html', {'book_list': book_list})


@login_check
def author_book_list(request, pk):
    '''
    展示某个出版社，出版的书籍
    :param request:
    :param pk:要展示出版社的ID
    :return:
    '''
    print(pk)
    book_list = models.Author(pk=pk).book_set.all()
    print(book_list)
    return render(request, 'publish_book_list.html', {'book_list': book_list})
