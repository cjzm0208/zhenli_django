from django.shortcuts import render, HttpResponse
from . import forms
from . import models
from django.shortcuts import redirect
import hashlib
import datetime, time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
import random
import logging
from . import commun
from django.db.models import Q
logger = logging.getLogger('django')

# import string
# from . import commun
# from django.views.decorators.cache import cache_page
# from django.db.models import Q
# from mollie.api.client import Client
# from django.utils import timezone
# import os
# import logging
# from . import app

def hash_code(s, salt='zhenliwenhua2020'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    obj = forms.login_form()
    get = request.GET
    if 'id' in get:
        action_affix = '?id=' + get['id'] + '&page=' + get['page'] + '&type=' + get['type']
    if request.method == 'POST':
        login_form = forms.login_form(request.POST)
        # password = request.POST.get('password')
        print(login_form)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            if models.compte.objects.filter(email=email).exists():
                user = models.compte.objects.get(email=email)
            else:
                message = '此账号不存在'
                return render(request, 'login/login.html', locals())
            # try:
            #     user = models.compte.objects.get(email=email)
            # except:
            #     message = '此账号不存在'
            #     return render(request, 'login/login.html', locals())
            if user.mots_passe == hash_code(password):
                request.session['is_login'] = True
                if user.role == 10:
                    request.session['user'] = {'id': user.id, 'role': user.role, 'nom': user.prenom,
                                               'visuel': user.visuel}
                    return redirect('/accueil/index/')
                elif user.role == 15:
                    request.session['user'] = {'id': user.id, 'role': user.role, 'nom': user.prenom,
                                               'visuel': user.visuel}
                    return redirect('/accueil/index/')
                elif user.role == 5 or user.role == 0:
                    request.session['user'] = {'id': user.id, 'role': user.role, 'nom': user.prenom,
                                               'visuel': user.visuel}
                    return redirect('/accueil/index/')
                else:
                    request.session['user'] = {'id': user.id, 'role': 20, 'nom': user.prenom}
                    if 'id' not in get:
                        return redirect('/')
                    else:
                        if get['page'] == 'contenu_magasin':
                            return redirect('/communaute/index/contenu/' + get['id'] + '/?type=' + get['type'])
            else:
                message = '账号和密码不匹配'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    return render(request, 'login/login.html', locals())


def register(request):
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if request.method != 'POST':
        inputs = models.index_login_input()
    else:
        data = request.POST
        data = data.copy()
        if data['mots_passe'] != data['refaire_motes_passe']:
            message = '两次密码输入不一致'
            inputs = models.index_login_input(data=data)
            return render(request, 'login/register.html', locals())
        else:
            si_email = models.compte.objects.filter(email=data['email']).count()
            if si_email:
                inputs = models.index_login_input(data=data)
                message = '邮箱已经存在'
                return render(request, 'login/register.html', locals())
            else:
                data['mots_passe'] = hash_code(data['mots_passe'])
                data['refaire_motes_passe'] = hash_code(str(random.randint(0, 10000000000000)))
                inputs = models.index_login_input(data=data)
                if inputs.is_valid():
                    inputs.save()
                    return redirect('/login/')
    return render(request, 'login/register.html', locals())


def oubile_mots(request):
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1)
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if request.method != 'POST':
        pass
    else:
        data = request.POST
        si = models.compte.objects.filter(email=data['email'])
        if (si):
            if '@' in data['email']:
                user = models.compte.objects.get(email=data['email'])
                src = "http://" + request.META[
                    'HTTP_HOST'] + '/oubile_mots_change/?email=' + user.email + '&key=' + user.refaire_motes_passe
                message = '<p style="text-align: center;"><strong>你好, ' + user.prenom + '</strong></p><p style="text-align: center;"><strong>这封邮件时为了你修改真理文化的密码。</strong></p><p style="text-align: center;"><strong><a href="' + src + '"> 点击 </a>重置密码</strong></p><p style="text-align: center;"><strong>真理文化</strong></p>'
                email_from = '真理文化<tianzhuasia@gmail.com>'
                email = EmailMessage(
                    '修改密码',  # 主题
                    message,  # 内容
                    email_from,
                    [data['email']],  # 邮件去往
                    reply_to=['tianzhuasia@gmail.com'],
                )
                email.content_subtype = "html"
                email.send()
                icone = 'suc'
                titre = "我们已经往你的邮箱中发送一封密码修改邮件。"
                message = "你可以通过此邮件修改密码"
                action = ""
                lien = "/oubile_mots/"
                lien_mots = "登录"
                return render(request, 'index/notice.html', locals())
            else:
                sms = commun.keyword(request)
                new_sms = sms.find(data['email'])
                return render(request, 'login/oubile_tel_change.html', locals())
        else:
            icone = 'faut'
            titre = "你输入的邮箱或手机号不存在。"
            message = "请重试"
            action = ""
            lien = "/"
            lien_mots = "主页"
            return render(request, 'index/notice.html', locals())
    return render(request, 'login/oubile.html', locals())


def oubile_mots_change(request):
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if request.method != 'POST':
        get = request.GET
        user = models.compte.objects.get(email=get['email'])
        if user.refaire_motes_passe == get['key']:
            return render(request, 'login/oubile_change.html', locals())
        else:
            icone = 'faut'
            titre = "此链接已经失效。"
            message = "请重试"
            action = ""
            lien = "/"
            lien_mots = " 主页"
            return render(request, 'index/notice.html', locals())
    else:
        get = request.GET
        data = request.POST
        models.compte.objects.filter(email=get['email']).update(mots_passe=hash_code(data["password"]),
                                                                refaire_motes_passe=hash_code(
                                                                    str(random.randint(0, 10000000000000))))
        icone = 'suc'
        titre = "密码修改成功"
        message = "谢谢使用"
        action = ""
        lien = "/"
        lien_mots = " 主页"
        return render(request, 'index/notice.html', locals())

def oubile_mots_tel_change(request):
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if request.method != 'POST':
        icone = 'faut'
        titre = "此链接已经失效。"
        message = "请重试"
        action = ""
        lien = "/"
        lien_mots = " 主页"
        return render(request, 'index/notice.html', locals())
    else:
        data = request.POST
        if models.verifi_code.objects.filter(tel=data['tel'],code=data['code'],date_creer__gte=datetime.datetime.now()-datetime.timedelta(minutes=30)).exists():
            models.compte.objects.filter(email=data['tel']).update(mots_passe=hash_code(data["password"]),
                                                                    refaire_motes_passe=hash_code(
                                                                        str(random.randint(0, 10000000000000))))
            icone = 'suc'
            titre = "密码修改成功"
            message = "谢谢使用"
            action = ""
            lien = "/"
            lien_mots = " 主页"
            return render(request, 'index/notice.html', locals())
        else:
            message_error="你输入的验证码错误，修改失败"
            return render(request, 'login/oubile_tel_change.html', locals())
    return render(request, 'index/notice.html', locals())
def logout(request):
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def accueil(request):
    is_login = request.session.get('is_login', False)
    user_info = request.session.get('user', False)
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    tuijian = models.article.objects.order_by('-date_motifier').filter(visuel__isnull=False,date_motifier__lte=datetime.datetime.now())[:5]
    slidephoto = models.article.objects.order_by('-date_motifier').filter(visuel__isnull=False,date_motifier__lte=datetime.datetime.now())[:9]
    slide_premier = [slidephoto[0]]
    slide_deuxeme = [slidephoto[1], slidephoto[2],slidephoto[3], slidephoto[4], slidephoto[5]]
    priere = models.article.objects.order_by('-date_motifier').filter(cathegorie=32,date_motifier__lte=datetime.datetime.now())[:1]
    zhengdao = models.article.objects.order_by('-date_motifier').filter(cathegorie=13,date_motifier__lte=datetime.datetime.now())[:1]
    jiaodian = models.article.objects.order_by('-date_motifier').filter(cathegorie=59,date_motifier__lte=datetime.datetime.now())[:1]
    news = cath_article(1, 4)
    news_cath=models.cathegorie.objects.order_by("ordre").filter(id__in=[9,57,59,66,87])
    new_caths_list=[]
    for un in news_cath:
        un_cath= {'id':un.id,'titre':un.titre,'contenu': cath_article(un.id, 5)}
        new_caths_list.append(un_cath)

    #证道
    homelies_cath = models.cathegorie.objects.order_by('ordre','id').filter(id__in=[13,85,83,14,12,154,236])
    homelies_caths_list = []
    for un in homelies_cath:
        un_cath = {'id': un.id, 'titre': un.titre, 'contenu': cath_article(un.id, 4)}
        homelies_caths_list.append(un_cath)
    # 圣经
        # 证道
    bibles_cath = models.cathegorie.objects.order_by('ordre','id').filter(id__in=[34,15,16,35,243,141])
    bibles_caths_list = []
    for un in bibles_cath:
        un_cath = {'id': un.id, 'titre': un.titre, 'contenu': cath_article(un.id, 5)}
        bibles_caths_list.append(un_cath)
    bibles = cath_article(2, 6)
    professions = cath_article(30, 8)
    zhongyao = cath_article(40, 1)
    familles = cath_article(37, 8)

    setting_commun=commun.Setting(request)
    settings=setting_commun.setting_index()
    # if is_login:
    #     user_info = request.session.get('user', None)
    #     messages = models.evenement.objects.filter(inscri_id=user_info['id'], lu_user=1).count()
    #     if (user_info['role'] > 18):
    #         gestion = False
    #     else:
    #         gestion = True
    # else:
    #     user_info = ""
    #     messages = 0
    # titre="Accueil"
    # message=0
    return render(request, 'index/index.html', locals())


def cath_article(parent, n):
    news_cathe = models.cathegorie.objects.filter(parent=parent)
    new_news_cathe = [parent]
    for un in news_cathe:
        new_news_cathe.append(un.id)
    articles = models.article.objects.order_by('-date_motifier').filter(cathegorie__in=new_news_cathe,date_motifier__lte=datetime.datetime.now()).distinct()[:n]
    return articles


def index(request, type, num, name):
    is_login = request.session.get('is_login', False)
    user_info = request.session.get('user', False)
    menus_cours = models.cathegorie_cours.objects.order_by('ordre').filter(observation=1).exclude(id__in=[1])
    menus = models.cathegorie.objects.order_by('ordre').filter(observation=1)
    aimes_acticle = models.article.objects.order_by('-lire').all()[:5]
    setting_commun = commun.Setting(request)
    settings = setting_commun.setting_general()
    if type == 'cathegory':
        if int(num):
            tag="cathegory"
            current=models.cathegorie.objects.get(id=num)
            if current.parent!=0:
                current1_show = True
                current1=models.cathegorie.objects.get(id=current.parent)
                if current1.parent!=0:
                    current2_show = True
                    current2=models.cathegorie.objects.get(id=current1.parent)
        get = request.GET
        if name=="搜索":
            data=request.POST
            get=get.copy()
            search_contenu=""
            if "search" in data:
                get["search"] = data["search"]
                search_contenu=data["search"]
            if "search" in get:
                search_contenu=get["search"]
            if search_contenu !="":
                articles = models.article.objects.order_by('-date_motifier').filter(Q(title__contains=search_contenu)|Q(contenu__contains=search_contenu),date_motifier__lte=datetime.datetime.now())
            else:
                articles=[]
                notice="你需要输入点内容进行搜索"
        else:
            value = models.cathegorie.objects.get(id=num)
            if (value.titre != name):
                return redirect('/home/')
            new_news_cathe = [num]
            if value.parent == 0:
                news_cathe = models.cathegorie.objects.filter(parent=num)
                for un in news_cathe:
                    new_news_cathe.append(un.id)
            articles = models.article.objects.order_by('-date_motifier').filter(cathegorie__in=new_news_cathe,date_motifier__lte=datetime.datetime.now()).distinct()
        recents = models.article.objects.order_by('-date_motifier').all()[:5]
        p = Paginator(articles, 12)
        if ('page' in get):
            page_num = get['page']
        else:
            page_num = 1
        page = p.page(page_num)
        return render(request, 'index/cathegory.html', locals())
    elif type == 'content':
        value = models.article.objects.get(id=num)
        cathegories=value.cathegorie.all()
        cathegories_list=[]
        for un in cathegories:
            cathegories_list.append(un.id)
        print(cathegories)
        get = request.GET
        show_bar=False
        tag = "cathegory"
        if "parent" in get:
            if int(get["parent"]):
                cathogorie_id=get["parent"]
                show_bar=True
            else:
                cathegories = value.cathegorie.all()
                cathegories_list = []
                for un in cathegories:
                    cathegories_list.append(un.id)
                if len(cathegories_list)>0:
                    show_bar = True
                    cathogorie_id=max(cathegories_list)
                else:
                    show_bar=False
            if show_bar:
                current = models.cathegorie.objects.get(id=cathogorie_id)
                if current.parent != 0:
                    current1_show = True
                    current1 = models.cathegorie.objects.get(id=current.parent)
                    if current1.parent != 0:
                        current2_show = True
                        current2 = models.cathegorie.objects.get(id=current1.parent)
        if value.visuel:
            value.visuel=value.visuel.replace("thumbnail","standard")
            logo=value.visuel.replace("standard-","icon-")
        # if (value.title != name):
        #     return redirect('/home/')
        models.article.objects.filter(id=value.id).update(lire=value.lire+1)
        recents = models.article.objects.order_by('-date_motifier').all()[:5]
        inti={'type':'article','parent':value.id,'title':value.title}
        if is_login:
            inti['user_id']=user_info['id']
        comment=models.comments_input(initial=inti)
        comments=models.comments.objects.filter(parent=num,parent_comment=0)
        for un in comments:
            res=chercher_subcomment(un)
            if not res:
                un=chercher_subcomment(un)
        return render(request, 'index/content.html', locals())
    elif type == 'cours':
        current = models.cathegorie_cours.objects.get(id=num)
        if current.parent.id != 1:
            current1_show=True
            current1 = models.cathegorie_cours.objects.get(id=current.parent.id)
            if current1.parent.id != 1:
                current2_show = True
                current2 = models.cathegorie_cours.objects.get(id=current1.parent.id)
        tag='cours'
        cour_cathe=models.cathegorie_cours.objects.get(id=num)
        name=cour_cathe.titre
        cours=models.cours.objects.order_by('-id').filter(parent=0,cathegorie=num,observation=1)
        get = request.GET
        p = Paginator(cours, 12)
        if ('page' in get):
            page_num = get['page']
        else:
            page_num = 1
        page = p.page(page_num)
        return render(request, 'index/cathegory.html', locals())
    elif type == 'cours_contenu':
        value = models.cours.objects.get(id=num)
        cathe_id=value.cathegorie.id
        if value.parent!=0:
            parent = models.cours.objects.get(id=value.parent)
            cathe_id=parent.cathegorie.id
        current = models.cathegorie_cours.objects.get(id=cathe_id)
        if current.parent.id != 1:
            current1_show = True
            current1 = models.cathegorie_cours.objects.get(id=current.parent.id)
            if current1.parent.id != 1:
                current2_show = True
                current2 = models.cathegorie_cours.objects.get(id=current1.parent.id)
        tag = 'cours'
        recents = models.article.objects.order_by('-date_motifier').all()[:5]
        # if (value.title != name):
        #     return redirect('/home/')
        models.cours.objects.filter(id=num).update(lire=value.lire + 1)
        if value.parent == 0:
            sub_cours=models.cours.objects.filter(parent=value.id)
        inti = {'type': 'cours', 'parent': value.id,'title':value.title}
        if is_login:
            inti['user_id'] = user_info['id']
        comment = models.comments_input(initial=inti)
        comments = models.comments.objects.filter(parent=num,parent_comment=0)
        for un in comments:
            res=chercher_subcomment(un)
            if not res:
                un=chercher_subcomment(un)
        return render(request, 'index/content.html', locals())
    elif type == 'appdl':
        return render(request, 'index/weixinTip_purjs.html', locals())
    elif type=='comments':
        is_login = request.session.get('is_login', False)
        if not is_login:
            return redirect('/home/')
        data=request.POST
        if data['type'] == 'article':
            value = models.article.objects.get(id=data['parent'])
        else:
            value = models.cours.objects.get(id=data['parent'])
        les_forms = models.comments_input(data=data)
        if les_forms.is_valid():
            les_forms.save()
        else:
            print(les_forms.errors)
            pass
        if data['type']=='article':
            return redirect('/index/content/'+str(value.id)+'/'+value.title)
        else:
            return redirect('/index/cours_contenu/' + str(value.id) + '/' + value.title)

def chercher_subcomment(un):
    if models.comments.objects.filter(parent_comment=un.id).exists():
        sub_comments=models.comments.objects.filter(parent_comment=un.id)
        un.sub_comment=sub_comments
        for une in sub_comments:
            res=chercher_subcomment(une)
            if not res:
                une.sub_comment=chercher_subcomment(une)
        return un
    else:
        un.sub_comment=False
        return False

def page(request,type):
    if type=='tv':
        return render(request, 'index/tv.html', locals())
