import os
import random
from functools import wraps

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *


def login_require(view):
    @wraps(view)
    def is_login(request, *args, **kwargs):
        if not request.session.get('uid'):
            return redirect('login')
        else:
            return view(request, *args, **kwargs)
    return is_login


def username_vaild(username):
    return True if not User.objects.filter(username=username) else False


def password_vaild(password, password_confirm):
    return True if password == password_confirm else False


def mail_vaild(username, mail):
    return True if User.objects.filter(username=username, mail=mail) else False


def operate_vaild(uid, password):
    user = User.objects.get(pk=uid)
    return user.validate(password)


def choice_captcha(basedir):
    ans_path = os.path.join(settings.CAPTCHA_DIR, 'ans')
    ans = random.choice(os.listdir(ans_path))
    uuid = os.path.splitext(ans)[0][3:]
    with open(os.path.join(ans_path, ans), 'r') as f:
        ques = f.readlines()[-1].split('=', 1)[-1].strip()
    return uuid, ques


def captcha_vaild(uuid, captcha_x, captcha_y):
    if not uuid or not captcha_x or not captcha_y:
        return False
    ans_path = os.path.join(settings.CAPTCHA_DIR, 'ans')
    ans = 'ans{0}.txt'.format(uuid)
    answer = {}
    with open(os.path.join(ans_path, ans), 'r') as f:
        for line in f.readlines():
            if line != '\n':
                ans = line.split('=')
                answer[ans[0].strip()] = ans[1].strip()
    if float(answer['ans_pos_x_1']) <= float(captcha_x) <= (float(answer['ans_width_x_1'])+float(answer['ans_pos_x_1'])) and \
        float(answer['ans_pos_y_1']) <= float(captcha_y) <= (float(answer['ans_height_y_1'])+float(answer['ans_pos_y_1'])):
        return True
    return False


def input_filter(cmd):
    for ban in settings.BLACK_LIST:
        if ban in cmd.lower():
            return None
    return cmd


def safe_eval(cmd):
    save_cmd = input_filter(cmd)
    if save_cmd is None:
        return '**WAF**'
    else:
        try:
            return eval(save_cmd) 
        except Exception:
            return 'SyntaxError'


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() and \
            captcha_vaild(request.session.get('captcha'), 
                request.POST.get('captcha_x'), 
                request.POST.get('captcha_y')):
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
                if not user.validate(form.cleaned_data['password']):
                    raise User.DoesNotExist
            except User.DoesNotExist:
                return HttpResponse('username or password wrong (￣_￣ )', status=400)
            request.session['uid'] = user.pk
            return redirect('user')
        else:
            return HttpResponse('parameters invaild (￣_￣ )', status=400)
    else:
        if request.session.get('uid'):
            return redirect('user')
        form = LoginForm()
        uuid, ques = choice_captcha(settings.CAPTCHA_DIR)
        request.session['captcha'] = uuid
        return render(request, 'login.html', {
            'form': form, 
            'raw_user': True,
            'uuid': uuid,
            'ques': ques})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and \
            captcha_vaild(request.session.get('captcha'), 
                request.POST.get('captcha_x'), 
                request.POST.get('captcha_y')) and \
            username_vaild(form.cleaned_data['username']) and \
            password_vaild(form.cleaned_data['password'], form.cleaned_data['password_confirm']):
            if form.cleaned_data.get('invite_user'):
                try:
                    user = User.objects.get(username=form.cleaned_data['invite_user'])
                except User.DoesNotExist:
                    return HttpResponse('inviter not found (￣_￣ )', status=400)
                else:
                    if user.invited < settings.INVITE_LIMIT:
                        user.invited += 1
                        user.integral += settings.INVITE_AWARD
                        user.save()
            user = User(username=form.cleaned_data['username'], mail=form.cleaned_data['mail'])
            user.set_pass(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            return HttpResponse('parameters invaild (￣_￣ )', status=400)
    else:
        if request.session.get('uid'):
            return redirect('user')
        form = RegisterForm()
        uuid, ques = choice_captcha(settings.CAPTCHA_DIR)
        request.session['captcha'] = uuid
        return render(request, 'register.html', {
            'form': form, 
            'raw_user': True,
            'uuid': uuid,
            'ques': ques})


@login_require
def logout(request):
    try:
        del request.session['captcha']
        del request.session['uid']
        del request.session['shopcar']
    except KeyError:
        pass
    return redirect('login')


def pass_reset(request):
    raw_user = True if not request.session.get('uid') else False
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid() and \
            captcha_vaild(request.session.get('captcha'), 
                request.POST.get('captcha_x'), 
                request.POST.get('captcha_y')) and \
            mail_vaild(form.cleaned_data['username'], form.cleaned_data['mail']) and \
            password_vaild(form.cleaned_data['password'], form.cleaned_data['password_confirm']):
            user = User.objects.get(username=form.cleaned_data['username'])
            user.set_pass(form.cleaned_data['password'])
            user.save()
            return redirect('{0}?success=1'.format(reverse('pass_reset')))
        else:
            return redirect('{0}?danger=1'.format(reverse('pass_reset')))
    else:
        form = ResetForm()
        uuid, ques = choice_captcha(settings.CAPTCHA_DIR)
        request.session['captcha'] = uuid
        return render(request, 'reset.html', {
            'form': form,
            'raw_user': raw_user,
            'uuid': uuid,
            'ques': ques,
            'success': request.GET.get('success'),
            'danger': request.GET.get('danger')})


@login_require
def user_change(request):
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        if form.is_valid() and \
            operate_vaild(request.session['uid'], form.cleaned_data['old_password']) and \
            password_vaild(form.cleaned_data['password'], form.cleaned_data['password_confirm']):
            user = User.objects.get(pk=request.session['uid'])
            user.set_pass(form.cleaned_data['password'])
            user.save()
            return render(request, 'change.html', {'form': form, 'success': 1})
        else:
            return render(request, 'change.html', {'form': form, 'danger': 1})
    else:
        form = ChangeForm()
        return render(request, 'change.html', {'form': form})


@login_require
def user_reset(request):
    user = User.objects.get(pk=request.session['uid'])
    if user.username != settings.INIT_ADMIN_USER:
        return HttpResponse('permission deny (￣_￣ )', status=400)
    user.integral = settings.INIT_INTEGRAL
    user.save()
    own = Owner.objects.filter(user=user)
    own.delete()
    return redirect('user')


@login_require
def user_debug(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.session['uid'])
        is_admin = True if user.username == settings.INIT_ADMIN_USER else False
        own = Owner.objects.filter(user=user)
        if own and max([o.amount for o in own]) > settings.INIT_INTEGRAL:
            is_super = True
        else:
            is_super = False
        if not is_admin or not is_super:
            return HttpResponse('permission deny (￣_￣ )', status=400)
        debug = safe_eval(request.POST.get('cmd'))
        return render(request, 'user.html', {'user': user, 'owns': own, 'is_admin': is_admin, 'is_super': is_super, 'debug': debug})
    else:
        return HttpResponse('permission deny (￣_￣ )', status=400)


@login_require
def user(request):
    user = User.objects.get(pk=request.session['uid'])
    is_admin = True if user.username == settings.INIT_ADMIN_USER else False
    own = Owner.objects.filter(user=user)
    if own and max([o.amount for o in own]) > settings.INIT_INTEGRAL:
        is_super = True
    else:
        is_super = False
    return render(request, 'user.html', {'user': user, 'owns': own, 'is_admin': is_admin, 'is_super': is_super})


def shop(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Commodity.objects.order_by('-pk'), 10)
    try:
        commoditys = paginator.page(page)
    except PageNotAnInteger:
        commoditys = paginator.page(1)
    except EmptyPage:
        commoditys = paginator.page(paginator.num_pages)
    raw_user = True if not request.session.get('uid') else False
    return render(request, 'index.html', {'commoditys': commoditys, 'raw_user': raw_user})


def info(request):
    try:
        commodity = Commodity.objects.get(pk=request.GET['id'])
    except Exception:
        template = '[UID:{request.session[uid]}] commodity '+request.GET['id']+' not found (=￣ω￣=)'
        return HttpResponse(template.format(request=request), status=400)
    raw_user = True if not request.session.get('uid') else False
    return render(request, 'info.html', {'commodity': commodity, 'raw_user': raw_user})


@csrf_exempt
@login_require
def pay(request):
    if request.POST.get('id') and request.POST.get('price'):
        try:
            Commodity.objects.get(pk=int(request.POST['id']))
        except Commodity.DoesNotExist:
            return HttpResponse('commodity not found (￣_￣ )', status=400)
        cur_amount = Commodity.objects.get(pk=request.POST['id']).amount
        cur_amount -= 1
        commodity = Commodity.objects.get(pk=request.POST['id'])
        commodity.amount = cur_amount
        if float(request.POST['price']) < 1:
            return HttpResponse('don\'t be so mean (=￣ω￣=)', status=400)
        cur_integral = User.objects.get(pk=request.session['uid']).integral
        cur_integral -= float(request.POST['price'])
        user = User.objects.get(pk=request.session['uid'])
        user.integral = cur_integral
        if user.username != settings.INIT_ADMIN_USER and cur_amount <= (settings.INIT_INTEGRAL - 10):
            return HttpResponse('you can only afford that 2333333', status=400)
        if cur_amount >= 0 and cur_integral >= 0:
            commodity.save()
            user.save()
            own, _ = Owner.objects.get_or_create(user=user, commodity=commodity)
            own.amount += 1
            own.save()
            return render(request, 'shopcar.html', {'success': 1})
        else:
            return render(request, 'shopcar.html', {'danger': 1})
    else:
        return render(request, 'shopcar.html', {'danger': 1})


@login_require
def seckill(request):
    if request.method == 'POST':
        try:
            commodity = Commodity.objects.get(pk=request.POST.get('id'))
        except Exception:
            return render(request, 'seckill.html', {'danger': 1})
        user = User.objects.get(pk=request.session['uid'])
        if user.integral - commodity.price < 0 or (user.username != settings.INIT_ADMIN_USER and commodity.amount < (settings.INIT_INTEGRAL - 10)) or commodity.amount <= 0:
            return render(request, 'seckill.html', {'danger': 1})
        if user.pay(commodity.price) >= 0 and commodity.sell(1):
            user.save()
            commodity.save()
            own, _ = Owner.objects.get_or_create(user=user, commodity=commodity)
            own.amount += 1
            own.save()
            return render(request, 'seckill.html', {'success': 1})
        else:
            return render(request, 'seckill.html', {'danger': 1})
    else:
        return render(request, 'seckill.html', {'alert': True, 'admin_mail': settings.INIT_ADMIN_MAIL})


@csrf_exempt
@login_require
def shopcar(request):
    if request.method == 'POST':
        shopcar = request.session.get('shopcar')
        if shopcar:
            commodity = next(serializers.deserialize('json', shopcar)).object
            user = User.objects.get(pk=request.session['uid'])
            if user.username != settings.INIT_ADMIN_USER and commodity.amount <= (settings.INIT_INTEGRAL - 10):
                return HttpResponse('you can only afford that 2333333', status=400)
            if user.pay(commodity.price) >= 0 and commodity.sell(1):
                user.save()
                commodity.save()
                own, _ = Owner.objects.get_or_create(user=user, commodity=commodity)
                own.amount += 1
                own.save()
                del request.session['shopcar']
                return render(request, 'shopcar.html', {'success': 1})
            return render(request, 'shopcar.html', {'commodity': commodity, 'danger': 1})
        else:
            return render(request, 'shopcar.html', {'danger': 1})
    else:
        shopcar = request.session.get('shopcar')
        if shopcar:
            commodity = next(serializers.deserialize('json', shopcar)).object
        else:
            commodity = None
        return render(request, 'shopcar.html', {'commodity': commodity})


@login_require
def shopcar_add(request):
    if not request.POST.get('id'):
        return HttpResponse('parameters invaild (￣_￣ )', status=400)
    try:
        commodity = Commodity.objects.get(pk=request.POST['id'])
    except Commodity.DoesNotExist:
        return HttpResponse('commodity not found (￣_￣ )', status=400)
    else:
        request.session['shopcar'] = serializers.serialize('json', [commodity])
        return redirect('shopcar')


def captcha(request):
    if not request.session.get('captcha'):
        return HttpResponse('parameters invaild (￣_￣ )', status=400)
    uuid = request.session['captcha']
    jpg = 'ques{0}.jpg'.format(uuid)
    jpgs_path = os.path.join(settings.CAPTCHA_DIR, 'jpgs')
    with open(os.path.join(jpgs_path, jpg), 'rb') as f:
        return HttpResponse(f.read(), content_type='image/jpeg')
