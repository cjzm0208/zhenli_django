from django.shortcuts import render,HttpResponse
from . import forms
from . import models
from . import commun
from django.shortcuts import redirect
# Create your views here.
import hashlib
import datetime,time
from django.conf import settings
import json
import os
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.core.mail import EmailMessage
from django.template import loader
import random
from django.forms.models import model_to_dict
from mutagen.mp3 import MP3
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import logging
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
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)
@csrf_exempt
def app(request,fun):
    # host = request.META['HTTP_HOST']
    host="http://" + "yzzhenli.org"
    if fun=='app_login':
        data = request.GET
        if models.compte.objects.filter(email=data['email']).exists():
            user=models.compte.objects.get(email=data['email'])
            if user.mots_passe==hash_code(data['mots_passe']):
                res=model_to_dict(user)
                res.pop('mots_passe')
                res.pop('refaire_motes_passe')
            else:
                res = "密码和邮箱不匹配"
        else:
            res="此邮箱账户不存在"
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='mon_info':
        data = request.GET
        user = models.compte.objects.get(id=data['id'])
        res = model_to_dict(user)
        res.pop('mots_passe')
        res.pop('refaire_motes_passe')
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='forget':
        data = request.GET
        si = models.compte.objects.filter(email=data['email'])
        if (si):
            if '@' in data['email']:
                user = models.compte.objects.get(email=data['email'])
                src = "http://" + request.META[
                    'HTTP_HOST'] + '/oubile_mots_change/?email=' + user.email + '&key=' + user.refaire_motes_passe
                message = '<p style="text-align: center;"><strong>你好, ' + user.prenom + '</strong></p><p style="text-align: center;"><strong>这封邮件时为了你修改真理文化的密码。</strong></p><p style="text-align: center;"><strong><a href="' + src + '"> 点击 </a>重置密码</strong></p><p style="text-align: center;"><strong>真理文化</strong></p>'
                email_from = 'Emergency Spi Par<emergency.spi@gmail.com>'
                email = EmailMessage(
                    '修改密码',  # 主题
                    message,  # 内容
                    email_from,
                    [data['email']],  # 邮件去往
                    reply_to=['tianzhuasia@gmail.com'],
                )
                email.content_subtype = "html"
                suc=email.send()
                if suc:
                    res='suc'
                else:
                    res='cuowu'
            else:
                sms = commun.keyword(request)
                new_sms = sms.find(data['email'])
                if new_sms:
                    res='yanzhengma'
                else:
                    res = 'cuowu'
        else:
            res='pas email'
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="forget_tel":
        data = request.GET
        if models.verifi_code.objects.filter(tel=data['tel'], code=data['code'],
                                             date_creer__gte=datetime.datetime.now() - datetime.timedelta(
                                                     minutes=30)).exists():
            res=models.compte.objects.filter(email=data['tel']).update(mots_passe=hash_code(data["password"]),
                                                                   refaire_motes_passe=hash_code(
                                                                       str(random.randint(0, 10000000000000))))
            if res:
                res="suc"
            else:
                res="faut"
        else:
            res="faut"
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun == 'modifier_info':
        data = request.GET
        new_data={}
        for key,val in data.items():
            new_data[key] = val
        new_data.pop('user_id')
        new_data['naissance']=datetime.datetime.strptime(new_data['naissance'], '%Y-%m-%d')
        models.compte.objects.filter(id=data['user_id']).update(**new_data)
        res=models.compte.objects.get(id=data['user_id'])
        res=model_to_dict(res)
        res.pop('mots_passe')
        res.pop('refaire_motes_passe')
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='app_creer_un_compte':
        data = request.GET
        data = data.copy()
        if data['mots_passe'] != data['refaire_motes_passe']:
            message = '两次密码输入不一致'
        else:
            si_email = models.compte.objects.filter(email=data['email']).count()
            if si_email:
                message = '邮箱已经存在'
            else:
                data['mots_passe'] = hash_code(data['mots_passe'])
                data['refaire_motes_passe'] = hash_code(str(random.randint(0, 10000000000000)))
                inputs = models.index_login_input(data=data)
                if inputs.is_valid():
                    res=inputs.save()
                    message = model_to_dict(res)
                    message="账号创建成功"
        return HttpResponse(json.dumps(message, cls=DateEncoder))
    elif (fun == "index"):
        tuijian = cath_article_index(8, 4)
        news = cath_article_index(9, 3)
        ask_petre=cath_article_index(30, 1)
        speaks=cath_article_index(59, 3)
        confessions=cath_article_index(13, 3)
        verites=cath_article_index(14, 3)
        dimanches=cath_article_index(12, 3)
        open_bibles=cath_article_index(15, 4)
        classiques = cath_article_index(20, 3)
        chretiens= cath_article_index(21, 3)
        familles= cath_article_index(22, 4)
        # familles = cath_article(22, 4)
        enfants= cath_article_index(25, 4)
        monde_chants= cath_article_index(7, 3)
        priere_unem= cath_article_index(32, 4)
        lives=models.live.objects.order_by('-id').filter(start__lte=datetime.datetime.now(),end__gte=datetime.datetime.now(),observation=1)[:1].values('id','title','start','end','visuel')
        values={'tuijian':tuijian,'news':news,'ask_petre':ask_petre,'speaks':speaks,'confessions':confessions,'verites':verites,'dimanches':dimanches,'open_bibles':open_bibles,'classiques':classiques,'chretiens':chretiens,'familles':familles,'enfants':enfants,'monde_chants':monde_chants,'priere_unem':priere_unem,'lives':list(lives)}
        return HttpResponse(json.dumps(values,cls=DateEncoder))
    elif fun=='post':
        data=request.GET
        value=models.article.objects.filter(id=data['id']).values()
        new_value=value[0]
        models.article.objects.filter(id=data['id']).update(lire=new_value['lire'] + 1)
        if(new_value['fichier_audio']):
            # src=new_value['fichier_audio']
            # src = src.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com", "static/upload");
            # src=src.replace("/static/", "static/");
            # audio = MP3(src)
            # duration = audio.info.length
            # new_value['duration']=int(duration)
            if new_value['fichier_audio']:
                if 'https' not in str(new_value['fichier_audio']):
                    new_value['fichier_audio'] = 'https://www.yzzhenli.org' + str(new_value['fichier_audio'])
                # new_value['fichier_audio'] = 'http://127.0.0.1:8000' + new_value['fichier_audio']
                # new_value['fichier_audio']='http://www.yzzhenli.org'+new_value['fichier_audio']
            if new_value['visuel']:
                if 'https' not in str(new_value['visuel']):
                    new_value['visuel'] = 'https://www.yzzhenli.org' + str(new_value['visuel'])
                # new_value['visuel'] = 'http://127.0.0.1:8000' + new_value['visuel']
                # new_value['visuel'] = 'http://www.yzzhenli.org' + new_value['visuel']
        return HttpResponse(json.dumps(new_value, cls=DateEncoder))
    elif fun=='category_post':
        data = request.GET
        values=cath_article(data['category_id'],data['limit'],data['n'])
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='category_post_audio_list':
        data = request.GET
        values=cath_article_audios_list(data['category_id'],data['limit'],data['n'])
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='category_cours_audio_list':
        data = request.GET
        values=models.cours.objects.filter(parent=data['category_id'],fichier_audio__contains='/').values()
        for un in values:
            if 'https' not in str(un['visuel']) and un['visuel']:
                un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
            if 'https' not in str(un['fichier_audio']) and un['fichier_audio']:
                un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
        values=list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='menu':
        menu=models.cathegorie.objects.order_by('ordre').filter(observation=1).values()
        menu=list(menu)
        return HttpResponse(json.dumps(menu, cls=DateEncoder))
    elif fun=='priere':
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        values=models.pray.objects.order_by('-id').filter()[n*limit:(n+1)*limit].values()
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='beni_priere':
        data = request.GET
        value=models.pray.objects.get(id=data['id'])
        if data['type']=='priere':
            models.pray.objects.filter(id=data['id']).update(payer=value.payer+1)
        else:
            models.pray.objects.filter(id=data['id']).update(louer=value.louer + 1)
        return HttpResponse(json.dumps('values', cls=DateEncoder))
    elif fun=='plubier_priere':
        data = request.POST
        user = models.compte.objects.get(id=data['user_id'])
        if user.role > 20:
            value = 'fail'
        else:
            res = models.pray.objects.create(contenu=data['contenu'], user_id=data['user_id'],
                                             user_name=data['user_name'])
            if res:
                value = 'suc'
            else:
                value = 'fail'
        return HttpResponse(json.dumps(value, cls=DateEncoder))
    elif fun=='mes_priere':
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        values=models.pray.objects.order_by('-id').filter(user_id=data['user_id'])[n*limit:(n+1)*limit].values()
        values=list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='sup_priere':
        data = request.GET
        val=models.pray.objects.get(id=data['id'])
        if(val.user_id==data['user_id']):
            models.pray.objects.filter(id=data['id']).delete()
            return HttpResponse(json.dumps('suc', cls=DateEncoder))
        else:
            return HttpResponse(json.dumps('fail', cls=DateEncoder))
    elif fun=='cours_list':
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        values=models.cours.objects.order_by("-id").filter(parent=0)[n*limit:(n+1)*limit].values()
        for un in values:
            if un["fichier_audio"]:
                if 'https' not in str(un['fichier_audio']):
                    un["fichier_audio"] = host + un["fichier_audio"]
            if un["visuel"]:
                if 'https' not in str(un['visuel']):
                    un["visuel"] = host + un["visuel"]
        values = list(values)
        print(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='cours_audios_list':
        data = request.GET
        values = models.cours.objects.filter(parent=data['id']).values()
        for un in values:
            if un["fichier_audio"]:
                if 'https' not in str(un['fichier_audio']):
                    un["fichier_audio"] = host + un["fichier_audio"]
            if un["visuel"]:
                if 'https' not in str(un['visuel']):
                    un["visuel"] = host + un["visuel"]
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='un_cours':
        data = request.GET
        values = models.cours.objects.filter(id=data['id']).values()
        new_value = values[0]
        if new_value["fichier_audio"]:
            if 'https' not in str(new_value['fichier_audio']):
                new_value["fichier_audio"] = host + new_value["fichier_audio"]
        if new_value["visuel"]:
            if 'https' not in str(new_value['visuel']):
                new_value["visuel"] = host + new_value["visuel"]
        # if (new_value['fichier_audio']):
        #     src = new_value['fichier_audio']
        #     src = src.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com", "static/upload");
        #     src = src.replace("/static/", "static/");
        #     audio = MP3(src)
        #     duration = audio.info.length
        #     new_value['duration'] = int(duration)
        return HttpResponse(json.dumps(new_value, cls=DateEncoder))
    elif fun=='search':
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        values = models.article.objects.order_by('-id').filter(Q(title__contains=data['key'])|Q(contenu__contains=data['key']))[n * limit:(n + 1) * limit].values()
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=="category_new":
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        if(data['type']=='直播'):
            values = models.live.objects.order_by('-id').filter()[n * limit:(n + 1) * limit].values()
        elif data['type'] == '我的直播':
            values = models.live.objects.order_by('-id').filter(professeur_id=data['user_id'])[n * limit:(n + 1) * limit].values()
        elif data['type'] == '课程':
            values = models.cours.objects.filter(parent=0)[n * limit:(n + 1) * limit].values()
            for un in values:
                if un["fichier_audio"]:
                    if 'https' not in un['fichier_audio']:
                        un["fichier_audio"] = host + un["fichier_audio"]
                if un["visuel"]:
                    if 'https' not in un['visuel']:
                        un["visuel"] = host + un["visuel"]
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='post_live':
        data = request.GET
        values = models.live.objects.filter(id=data['id']).values()
        values=list(values)
        return HttpResponse(json.dumps(values[0], cls=DateEncoder))
    elif fun=='fankui':
        data = request.GET
        res=models.feedback.objects.create(email=data['email'],contenu=data['contenu'],user_name=data['user_name'],date_motifier=datetime.datetime.now(),date_creer=datetime.datetime.now(),user_id=data['user_id'])
        if res:
            re='suc'
        else:
            re='fail'
        return HttpResponse(json.dumps(re, cls=DateEncoder))
    elif fun=='shoucang':
        data = request.GET
        res=models.favorise.objects.create(post_id=data['post_id'],user_id=data['user_id'],type=data['type'],date_creer=datetime.datetime.now())
        if res:
            re='suc'
        else:
            re='fail'
        return HttpResponse(json.dumps(re, cls=DateEncoder))
    elif fun=="fankui_list":
        data = request.GET
        res=models.feedback.objects.order_by('-id').filter(user_id=data['user_id']).values()
        for un in res:
            if models.feedback.objects.filter(parent=un['id']):
                un['sub_comment'] = list(
                    models.feedback.objects.filter(parent=un['id']).values())
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='sishoucang':
        data = request.GET
        if models.favorise.objects.filter(post_id=data['post_id'],user_id=data['user_id'],type=data['type']).exists():
            res=1
        else:
            res=0
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='list_shoucang':
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        favorises=models.favorise.objects.order_by('-id').filter(user_id=data['user_id'])[
                   n * limit:(n + 1) * limit]
        res=[]
        for un in favorises:
            if un.type=='post':
                une=models.article.objects.get(id=un.post_id)
                res.append({'id':une.id,'title':une.title,'visuel':une.visuel,'type':'post'})
            elif un.type=='cours':
                une=models.cours.objects.get(id=un.post_id)
                res.append({'id':une.id,'title': une.title, 'visuel': une.visuel,'type':'cours'})
            elif un.type == '直播':
                une = models.live.objects.get(id=un.post_id)
                res.append({'id':une.id,'title': une.title, 'visuel': une.visuel,'type':'直播'})
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='write_share':
        data = request.GET
        if data['type']=="post":
            value=models.article.objects.get(id=data['id'])
            res=models.comments.objects.create(contenu=data['contenu'],user_id=models.compte.objects.get(id=data['user_id']),parent=data['id'],date_creer=datetime.datetime.now(),type='article',title=value.title)
            res=model_to_dict(res)
        else:
            value = models.cours.objects.get(id=data['id'])
            res = models.comments.objects.create(contenu=data['contenu'],
                                                 user_id=models.compte.objects.get(id=data['user_id']),
                                                 parent=data['id'],
                                                 date_creer=datetime.datetime.now(), type=data['type'],title=value.title)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="share_lists":
        res=[]
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        data=data.copy()
        if data['type'] == "post":
            data['type']='article'
        res=models.comments.objects.order_by('-id').filter(parent=data['id'],parent_comment=0,type=data['type'])[n * limit:(n + 1) * limit].values('id','contenu','user_id__prenom','user_id__visuel','user_id','date_creer')
        for un in res:
            if models.comments.objects.filter(parent_comment=un['id']):
                un['sub_comment']=list(models.comments.objects.filter(parent_comment=un['id']).values('id','contenu','user_id__prenom','user_id__visuel','user_id','date_creer'))
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="mes_shares":
        res=[]
        data = request.GET
        limit = int(data['limit'])
        n = int(data['n'])
        res=models.comments.objects.order_by('-id').filter(user_id=data['user_id'],parent_comment=0)[n * limit:(n + 1) * limit].values('contenu','user_id__prenom','user_id__visuel','user_id','date_creer','id','title')
        for un in res:
            if models.comments.objects.filter(parent_comment=un['id']):
                un['sub_comment'] = list(
                    models.comments.objects.filter(parent_comment=un['id']).values('id', 'contenu',
                                                                                           'user_id__prenom',
                                                                                           'user_id__visuel', 'user_id',
                                                                                           'date_creer'))
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="sup_comments":
        data = request.GET
        val=models.comments.objects.get(id=data['id'])
        res=0
        if val.user_id.id==int(data['user_id']):
            res=models.comments.objects.get(id=data['id']).delete()
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='tuijian':
        menu_data=models.setting.objects.get(key="zhuda_cathe")
        menu=json.loads(menu_data.contenu)
        new_menu=[]
        for un in menu:
            cathe=models.cathegorie.objects.get(id=un)
            new_menu.append({"id":un,"titre":cathe.titre})
        print(new_menu)
        return HttpResponse(json.dumps(new_menu, cls=DateEncoder))

@csrf_exempt
def app_help(request,fun):
    if (fun == "uploadfile"):
        if request.method == "POST":
            post = request.POST
            file_obj = request.FILES.get("file")
            reqfile = request.FILES.get("file")
            path = 'static/upload/icone/'
            if not os.path.exists(path):
                os.mkdir(path)
            file_type = os.path.splitext(path + post['user_id'] + '-' + reqfile.name)[-1][1:]
            file_type = file_type.lower()
            if (post['type'] == 'icone'):
                image = Image.open(reqfile)
                image.save(path + post['user_id'] + "." + file_type)
                if (image.width / image.height > 1.5):
                    zoom = image.resize((image.width * 300 // image.height, 300))
                    box = ((zoom.width - 300) / 2, 0, (zoom.width - 300) / 2 + 300, 300)  ##确定拷贝区域大小
                    couper = zoom.crop(box)
                else:
                    zoom = image.resize((300, image.height * 300 // image.width))
                    box = (0, (zoom.height - 300) / 2, 300, (zoom.height - 300) / 2 + 300)  ##确定拷贝区域大小
                    couper = zoom.crop(box)
                couper.save(path + post['user_id'] + '-' + 'standard' + "." + file_type)
                couper.thumbnail((150, 150), Image.ANTIALIAS)
                couper.save(path + post['user_id'] + '-' + 'thumbnail' + "." + file_type)
                models.compte.objects.filter(id=post['user_id']).update(visuel='/'+path + post['user_id'] + '-' + 'thumbnail' + "." + file_type)
        return HttpResponse(json.dumps('res', cls=DateEncoder))
    elif fun == 'update':
        data = request.POST
        if data['platform']=='android':
            if data['version']<'2.0.8':
                res = {
                    'code': 0,
                    'msg': "更新内容：重新制作了app，使播放更加流畅。新app需要重新安装，安装完之后请删除旧app。",
                    'version': '2.0.8',  # // 版本号
                    'url': 'https://yzzhenli.org/static/upload/commun/zhenliwenhua.apk',  # // url下载地址，wgt优先，如果不存在新wgt，并且是ios，则此处为AppStore的地址 http...apk|wgt
                    'log': '更新内容：\n重新制作app使播放更加流畅。\n修复很多功能。\n希望你尽快更新。\n新app需要重新安装，安装完之后请删除旧app。',  # // 更新文字说明，支持 \n换行
                    'force': 0,  # 是否强制升级，force = 1 则是强制升级，用户无法关闭升级提示框
                }
            else:
                res={
                        'code': 1,
                        'msg': "no"
                    }
        else:
            res = {
                'code': 1,
                'msg': "no"
            }
        return HttpResponse(json.dumps(res, cls=DateEncoder))
            # elif (file_type == "mp3" or file_type == "wma"):
            #     type = 'audio'
            #     with open(path + now + '-' + reqfile.name, "wb") as f:
            #         for line in reqfile:
            #             f.write(line)
            #     print(path + now + '-' + reqfile.name)
            #     audio = MP3(path + now + '-' + reqfile.name)
            #     duration = audio.info.length
            #     stantard = 'audio.jpg'
            #     thumb = 'audio.jpg'
            # else:
            #     type = file_type
            #     duration = 0
            #     thumb = file_type + '.jpg'
            #     stantard = file_type + '.jpg'
            #     with open(path + now + '-' + reqfile.name, "wb") as f:
            #         for line in reqfile:
            #             f.write(line)
            # obj = models.dossiers(
            #     nom_org=reqfile,
            #     nom=now + "-" + reqfile.name,
            #     type=type,
            #     lien='/' + path,
            #     duration=duration,
            #     stantard=stantard,
            #     thumb=thumb,
            #     user_id=user_info['id'],
            # )
            # obj.save()
            # if (obj.id):
            #     res = "suc"
            # else:
            #     res = "fail"
def cath_article_index(parent,n):
    all_cathe = models.cathegorie.objects.all()
    # news_cathe = models.cathegorie.objects.filter(parent=parent)
    new_news_cathe = [parent]
    for un in all_cathe:
        if un.parent == parent:
            new_news_cathe.append(un.id)
            for un2 in all_cathe:
                if un2.parent == un.id:
                    new_news_cathe.append(un2.id)
    articles=models.article.objects.order_by('-date_motifier').filter(cathegorie__in=new_news_cathe,date_motifier__lte=datetime.datetime.now())[:n].values('id','title','visuel')
    for un in articles:
        if 'https' not in str(un['visuel']):
            un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
    articles = list(articles)
    return articles

def cath_article(parent,limit,n):
    parent=int(parent)
    limit = int(limit)
    n = int(n)
    all_cathe=models.cathegorie.objects.all()
    # news_cathe = models.cathegorie.objects.filter(parent=parent)
    new_news_cathe = [parent]
    for un in all_cathe:
        if un.parent==parent:
            new_news_cathe.append(un.id)
            for un2 in all_cathe:
                if un2.parent==un.id:
                    new_news_cathe.append(un2.id)
    articles=models.article.objects.order_by('-date_motifier','-id').filter(cathegorie__in=new_news_cathe,date_motifier__lte=datetime.datetime.now())[n*limit:(n+1)*limit].values()
    for un in articles:
        if 'https' not in str(un['visuel']):
            un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
        if 'https' not in str(un['fichier_audio']):
            un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
    articles = list(articles)
    return articles

def cath_cours(parent,limit,n):
    print(parent,limit,n)
    parent=int(parent)
    limit = int(limit)
    n = int(n)
    news_cathe = models.cathegorie_cours.objects.filter(parent=parent)
    new_news_cathe = [parent]
    for un in news_cathe:
        new_news_cathe.append(un.id)
    print(new_news_cathe)
    articles=models.cours.objects.order_by('-date_motifier','-id').filter(cathegorie__in=new_news_cathe)[n*limit:(n+1)*limit].values()
    for un in articles:
        if 'https' not in str(un['visuel']):
            un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
        if 'https' not in str(un['fichier_audio']):
            un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
    articles = list(articles)
    return articles

def cath_article_audios_list(parent,limit,n):
    parent=int(parent)
    limit = int(limit)
    n = int(n)
    articles=models.article.objects.order_by('-id').filter(Q(cathegorie=parent,date_motifier__lte=datetime.datetime.now()),~Q(fichier_audio=None))[n*limit:(n+1)*limit].values()
    for un in articles:
        if 'https' not in str(un['visuel']) and un['visuel']:
            un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
        if 'https' not in str(un['fichier_audio']) and un['fichier_audio']:
            un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
    articles = list(articles)
    return articles

@csrf_exempt
def apps(request,fun):
    host = request.META['HTTP_HOST']
    host="http://" + "yzzhenli.org"
    res=""
    if fun=="last":
        logger.error("last")
        last=models.article.objects.order_by("-id").all()[:20].values()
        res = list(last)
    elif fun=='app_creer_un_compte':
        data = request.POST
        data = data.copy()
        message="fail"
        si_email = models.compte.objects.filter(email=data['email']).count()
        if si_email:
            message = 'Email_exsit'
        else:
            data['mots_passe'] = hash_code(data['mots_passe'])
            data['refaire_motes_passe'] = hash_code(str(random.randint(0, 10000000000000)))
            inputs = models.index_login_input(data=data)
            if inputs.is_valid():
                res=inputs.save()
                message = model_to_dict(res)
                message="suc"
        return HttpResponse(json.dumps(message, cls=DateEncoder))
    if fun=='app_login':
        data = request.POST
        if models.compte.objects.filter(email=data['email']).exists():
            user=models.compte.objects.get(email=data['email'])
            logger.error(user.__dict__)
            if user.mots_passe==hash_code(data['mots_passe']):
                res=model_to_dict(user)
                logger.error(res)
                res.pop('mots_passe')
                res.pop('refaire_motes_passe')
            else:
                res = "email_mot"
        else:
            res="pas_email"
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="article":
        data=request.POST
        value = models.article.objects.filter(id=data['id']).values()
        res = value[0]
        if 'https' not in str(res['fichier_audio']) and res['fichier_audio']:
            res['fichier_audio'] = 'https://www.yzzhenli.org' + str(res['fichier_audio'])
        if res['fichier_video']:
            res['fichier_video']=res['fichier_video'].replace("http://","https://")
    elif fun=="index":
        tuijian = cath_article_index(8, 4)
        ask_petre = cath_article_index(30, 1)
        news = cath_article_index(9, 3)
        speaks = cath_article_index(59, 3)
        confessions = cath_article_index(13, 3)
        verites = cath_article_index(14, 3)
        dimanches = cath_article_index(12, 3)
        open_bibles = cath_article_index(15, 4)
        classiques = cath_article_index(20, 3)
        chretiens = cath_article_index(21, 3)
        familles = cath_article_index(22, 4)
        # familles = cath_article(22, 4)
        enfants = cath_article_index(25, 4)
        monde_chants = cath_article_index(7, 3)
        priere_unem = cath_article_index(32, 4)
        res={"tuijian":tuijian,"list":
            [{"title":"问问神父","data":ask_petre,"type":1,"id":30},
             {"title":"每日新闻","data":news,"type":3,"id":9},
            {"title": "听教宗讲道", "data": speaks, "type": 3,"id":59},
            {"title": "每日反省", "data": confessions, "type": 3,"id":13},
             {"title": "真理讲道台", "data": verites, "type": 3,"id":14},
             {"title": "主日证道", "data": dimanches, "type": 3,"id":12},
             {"title": "打开圣经", "data": open_bibles, "type": 4,"id":15},
             {"title": "中国经典", "data": classiques, "type": 3,"id":20},
             {"title": "基督徒看天下", "data": chretiens, "type": 3,"id":21},
             {"title": "家庭课堂", "data": familles, "type": 4,"id":22},
             {"title": "儿童故事", "data": enfants, "type": 4,"id":25},
             {"title": "最新华语歌曲", "data": monde_chants, "type": 3,"id":7},
             {"title": "一分钟祈祷", "data": priere_unem, "type": 4,"id":32},
             ]}
        menus=models.cathegorie.objects.filter(observation=1,parent=0)
        new_menus=[]
        for un in menus:
            new_menus.append([un.id,un.titre])
        res["menus"]=new_menus
    elif fun=='category_post':
        data = request.POST
        values=cath_article(data['category_id'],data['limit'],data['n'])
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='new_category_post':
        data = request.POST
        print(data)
        if data["type"]=="article":
            cathe=models.cathegorie.objects.get(id=data['category_id'])
            # if cathe.parent == 0:
            #     parent=cathe.id
            # else:
            #     parent=cathe.parent
            cathegorie=models.cathegorie.objects.filter(parent=data['category_id']).order_by("ordre").values("id","titre","visuel")
            cathegorie=list(cathegorie)
            for un in cathegorie:
                if un["visuel"]:
                    if "https" not in str(un["visuel"]):
                        un["visuel"]="https://www.yzzhenli.org"+str(un["visuel"])
                else:
                    random_number = random.randint(1, 6)
                    un["visuel"] = f"https://www.yzzhenli.org/static/upload/commun/cathegorie{random_number}.jpg"
            if cathe.parent == 0:
                vrai_id = cathegorie[0]["id"]
            else:
                vrai_id = data['category_id']
            values = cath_article(vrai_id, data['limit'], data['n'])
            res={"titre":cathe.titre,"data":values,"cathegorie":cathegorie,"vrai_id":vrai_id}
        elif data["type"]=="cours":
            cathe = models.cathegorie_cours.objects.get(id=data['category_id'])
            cathegorie=models.cours.objects.filter(cathegorie=data['category_id'],parent=0).values("id", "titre",
                                                                                                  "visuel")
            if cathe.parent == 1:
                parent = cathe.id
            else:
                parent = cathe.parent
            pass
            cathegorie = models.cathegorie_cours.objects.filter(parent=parent).exclude(id=1).order_by("ordre").values("id", "titre",
                                                                                                  "visuel")
            cathegorie = list(cathegorie)
            for un in cathegorie:
                if "https" not in str(un["visuel"]):
                    un["visuel"]="http://10.0.3.2:8000"+str(un["visuel"])
            if cathe.parent == 0:
                vrai_id = cathegorie[0]["id"]
            else:
                vrai_id = data['category_id']
            values = cath_cours(vrai_id, data['limit'], data['n'])
            res = {"titre": cathe.titre, "data": values, "cathegorie": cathegorie, "vrai_id": vrai_id}
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='category_post_audio_list':
        data = request.POST
        values=cath_article_audios_list(data['category_id'],data['limit'],data['n'])
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='category_cours_audio_list':
        data = request.POST
        values=models.cours.objects.filter(parent=data['category_id'],fichier_audio__contains='/').values()
        for un in values:
            if 'https' not in str(un['visuel']) and un['visuel']:
                un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
            if 'https' not in str(un['fichier_audio']) and un['fichier_audio']:
                un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
        values=list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='priere':
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        user_limit=[3467,3789]
        if user_limit in [3467,3789]:
            values=models.pray.objects.order_by('-id')[n*limit:(n+1)*limit].values()
        else:
            values = models.pray.objects.order_by('-id').exclude(user_id__in=user_limit)[
                     n * limit:(n + 1) * limit].values()
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='beni_priere':
        data = request.POST
        value=models.pray.objects.get(id=data['id'])
        if data['type']=='priere':
            models.pray.objects.filter(id=data['id']).update(payer=value.payer+1)
        else:
            models.pray.objects.filter(id=data['id']).update(louer=value.louer + 1)
        return HttpResponse(json.dumps('values', cls=DateEncoder))
    elif fun=='plubier_priere':
        data = request.POST
        user = models.compte.objects.get(id=data['user_id'])
        if user.role > 20:
            value = 'fail'
        else:
            res = models.pray.objects.create(contenu=data['contenu'], user_id=data['user_id'],
                                             user_name=data['user_name'])
            if res:
                value = 'suc'
            else:
                value = 'fail'
        return HttpResponse(json.dumps(value, cls=DateEncoder))
    elif fun=='mes_priere':
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        values=models.pray.objects.order_by('-id').filter(user_id=data['user_id'])[n*limit:(n+1)*limit].values()
        values=list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='sup_priere':
        data = request.POST
        val=models.pray.objects.get(id=data['id'])
        if(val.user_id==data['user_id']):
            models.pray.objects.filter(id=data['id']).delete()
            return HttpResponse(json.dumps('suc', cls=DateEncoder))
        else:
            return HttpResponse(json.dumps('fail', cls=DateEncoder))
    elif fun=='cours_list':
        data = request.POST
        # limit = int(data['limit'])
        limit=50
        n = int(data['n'])
        values=models.cours.objects.order_by("-id").filter(parent=0)[n*limit:(n+1)*limit].values()
        for un in values:
            if un["fichier_audio"]:
                if 'https' not in str(un["fichier_audio"]):
                    un["fichier_audio"] = host + un["fichier_audio"]
            if un["visuel"]:
                if 'https' not in str(un["visuel"]):
                    un["visuel"] = host + un["visuel"]
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='cours_audios_list':
        data = request.POST
        values = models.cours.objects.filter(parent=data['id']).values()
        for un in values:
            if un["fichier_audio"]:
                if 'https' not in str(un["fichier_audio"]):
                    un["fichier_audio"] = host + un["fichier_audio"]
            if un["visuel"]:
                if 'https' not in str(un["visuel"]):
                    un["visuel"] = host + un["visuel"]
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='un_cours':
        data = request.POST
        values = models.cours.objects.filter(id=data['id']).values()
        new_value = values[0]
        if new_value["fichier_audio"]:
            if 'https' not in str(new_value['fichier_audio']):
                new_value["fichier_audio"] = host + new_value["fichier_audio"]
        if new_value["visuel"]:
            if 'https' not in str(new_value['visuel']):
                new_value["visuel"] = host + new_value["visuel"]
        # if (new_value['fichier_audio']):
        #     src = new_value['fichier_audio']
        #     src = src.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com", "static/upload");
        #     src = src.replace("/static/", "static/");
        #     audio = MP3(src)
        #     duration = audio.info.length
        #     new_value['duration'] = int(duration)
        print(new_value['fichier_audio'])
        return HttpResponse(json.dumps(new_value, cls=DateEncoder))
    elif fun=='search':
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        values = models.article.objects.order_by('-id').filter(Q(title__contains=data['key'])|Q(contenu__contains=data['key']))[n * limit:(n + 1) * limit].values()
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=="category_new":
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        if(data['type']=='直播'):
            values = models.live.objects.order_by('-id').filter()[n * limit:(n + 1) * limit].values()
        elif data['type'] == '我的直播':
            values = models.live.objects.order_by('-id').filter(professeur_id=data['user_id'])[n * limit:(n + 1) * limit].values()
        elif data['type'] == '课程':
            values = models.cours.objects.filter(parent=0)[n * limit:(n + 1) * limit].values()
            for un in values:
                if un["fichier_audio"]:
                    if 'https' not in str(un["fichier_audio"]):
                        un["fichier_audio"] = host + un["fichier_audio"]
                if un["visuel"]:
                    if 'https' not in str(un["visuel"]):
                        un["visuel"] = host + un["visuel"]
        values = list(values)
        return HttpResponse(json.dumps(values, cls=DateEncoder))
    elif fun=='post_live':
        data = request.POST
        values = models.live.objects.filter(id=data['id']).values()
        values=list(values)
        return HttpResponse(json.dumps(values[0], cls=DateEncoder))
    elif fun=='fankui':
        data = request.POST
        res=models.feedback.objects.create(contenu=data['contenu'],user_name=data['user_name'],date_motifier=datetime.datetime.now(),date_creer=datetime.datetime.now(),user_id=data['user_id'])
        if res:
            re='suc'
        else:
            re='fail'
        return HttpResponse(json.dumps(re, cls=DateEncoder))
    elif fun=='shoucang':
        data = request.POST
        res=models.favorise.objects.create(post_id=data['post_id'],user_id=data['user_id'],type=data['type'],date_creer=datetime.datetime.now())
        if res:
            re='suc'
        else:
            re='fail'
        return HttpResponse(json.dumps(re, cls=DateEncoder))
    elif fun=="fankui_list":
        data = request.POST
        res=models.feedback.objects.order_by('-id').filter(user_id=data['user_id']).values()
        for un in res:
            if models.feedback.objects.filter(parent=un['id']):
                un['sub_comment'] = list(
                    models.feedback.objects.filter(parent=un['id']).values())
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='sishoucang':
        data = request.POST
        if models.favorise.objects.filter(post_id=data['post_id'],user_id=data['user_id'],type=data['type']).exists():
            res=1
        else:
            res=0
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='list_shoucang':
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        favorises=models.favorise.objects.order_by('-id').filter(user_id=data['user_id'])[
                   n * limit:(n + 1) * limit]
        res=[]
        for un in favorises:
            if un.type=='post':
                une=models.article.objects.get(id=un.post_id)
                res.append({'id':une.id,'title':une.title,'visuel':une.visuel,'type':'post'})
            elif un.type=='cours':
                une=models.cours.objects.get(id=un.post_id)
                res.append({'id':une.id,'title': une.title, 'visuel': une.visuel,'type':'cours'})
            elif un.type == '直播':
                une = models.live.objects.get(id=un.post_id)
                res.append({'id':une.id,'title': une.title, 'visuel': une.visuel,'type':'直播'})
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='write_share':
        data = request.POST
        logger.error(data)
        if data['type']=="post":
            value=models.article.objects.get(id=data['id'])
            res=models.comments.objects.create(contenu=data['contenu'],user_id=models.compte.objects.get(id=data['user_id']),parent=data['id'],date_creer=datetime.datetime.now(),type='article',title=value.title)
            res=model_to_dict(res)
        else:
            value = models.cours.objects.get(id=data['id'])
            res = models.comments.objects.create(contenu=data['contenu'],
                                                 user_id=models.compte.objects.get(id=data['user_id']),
                                                 parent=data['id'],
                                                 date_creer=datetime.datetime.now(), type=data['type'],title=value.title)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="share_lists":
        res=[]
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        data=data.copy()
        if data['type'] == "post":
            data['type']='article'
        res=models.comments.objects.order_by('-id').filter(parent=data['id'],parent_comment=0,type=data['type'])[n * limit:(n + 1) * limit].values('id','contenu','user_id__prenom','user_id__visuel','user_id','date_creer')
        for un in res:
            if models.comments.objects.filter(parent_comment=un['id']):
                un['sub_comment']=list(models.comments.objects.filter(parent_comment=un['id']).values('id','contenu','user_id__prenom','user_id__visuel','user_id','date_creer'))
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="mes_shares":
        res=[]
        data = request.POST
        limit = int(data['limit'])
        n = int(data['n'])
        res=models.comments.objects.order_by('-id').filter(user_id=data['user_id'],parent_comment=0)[n * limit:(n + 1) * limit].values('contenu','user_id__prenom','user_id__visuel','user_id','date_creer','id','title')
        for un in res:
            if models.comments.objects.filter(parent_comment=un['id']):
                un['sub_comment'] = list(
                    models.comments.objects.filter(parent_comment=un['id']).values('id', 'contenu',
                                                                                           'user_id__prenom',
                                                                                           'user_id__visuel', 'user_id',
                                                                                           'date_creer'))
        res=list(res)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=="sup_comments":
        data = request.POST
        val=models.comments.objects.get(id=data['id'])
        res=0
        if val.user_id.id==int(data['user_id']):
            res=models.comments.objects.get(id=data['id']).delete()
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif fun=='tuijian':
        menu_data=models.setting.objects.get(key="zhuda_cathe")
        menu=json.loads(menu_data.contenu)
        new_menu=[]
        for un in menu:
            cathe=models.cathegorie.objects.get(id=un)
            new_menu.append({"id":un,"titre":cathe.titre})
        print(new_menu)
        return HttpResponse(json.dumps(new_menu, cls=DateEncoder))
    elif fun == "buildNumber":
        version = {'android': {'version': 6, 'adresse': 'https://yzzhenli.org/static/upload/commun/zhenliwenhua.apk',
                               'explication': '1.加入下载功能\n2.调整了视频播放中断问题\n'},
                   'ios': {'version': 1, 'adresse': 'http', 'explication': ''}}
        return HttpResponse(json.dumps(version))
    elif fun=="SameCathe":
        data = request.POST
        article=models.article.objects.get(id=data["id"])
        cathe = article.cathegorie.all()
        cathe_id = 8
        for un in cathe:
            if un.id != cathe_id:
                cathe_id = un.id
        values = cath_article(cathe_id, 10, 0)
        parent = cathe_id
        limit = 10
        n = 0
        news_cathe = models.cathegorie.objects.filter(parent=parent)
        new_news_cathe = [parent]
        for un in news_cathe:
            new_news_cathe.append(un.id)
        articles = models.article.objects.order_by('-id').filter(cathegorie__in=new_news_cathe,
                                                                                   date_motifier__lte=datetime.datetime.now(),id__lte=data["id"])[
                   n * limit:(n + 1) * limit].values()
        for un in articles:
            if 'https' not in str(un['visuel']):
                un['visuel'] = 'https://www.yzzhenli.org' + str(un['visuel'])
            if 'https' not in str(un['fichier_audio']):
                un['fichier_audio'] = 'https://www.yzzhenli.org' + str(un['fichier_audio'])
        articles = list(articles)
        return HttpResponse(json.dumps(articles, cls=DateEncoder))
    elif fun=="chapter":
        res = ""
        data = request.POST
        print(data)
        chapter=data.getlist("chapter")
        if data["page"]=="prev":
            if int(chapter[1])==1:
                current_book = models.sg_bibleBook.objects.get(mark=chapter[0])
                new_current_book = models.sg_bibleBook.objects.order_by("-id").filter(id__lt=current_book.id).first()
                last=models.sg_bibleBook.objects.filter(livre=new_current_book.mark).last()
                chapter = [new_current_book.mark, last.chapitre]
            else:
                chapter = [chapter[0], int(chapter[1]) - 1]
        elif data["page"]=="next":
            chapter=[chapter[0],int(chapter[1])+1]
            if models.sg_bible.objects.filter(livre=chapter[0],chapitre=chapter[1]).exists():
                pass
            else:
                current_book=models.sg_bibleBook.objects.get(mark=chapter[0])
                new_current_book=models.sg_bibleBook.objects.filter(id__gt=current_book.id).first()
                chapter = [new_current_book.mark, 1]
        res=[]
        #第一本书
        bible_model = getattr(models,"sg_bible")
        bible = bible_model.objects.filter(livre=chapter[0], chapitre=chapter[1])
        commun_mark=[]
        for un in bible:
            if un.commun:
                commun_mark.append(un.commun)
        print(commun_mark)
        Bible_contenu_list={}
        bibleBook_model = getattr(models, "sg_bibleBook")
        bibleBook=bibleBook_model.objects.get(mark=chapter[0])
        bible_model = getattr(models,"sg_bible")
        bible=bible_model.objects.order_by("-date").filter(Q(book__id=bibleBook.id,chapitre=chapter[1])|Q(commun__in=commun_mark)).values()
        Bible_contenu_list={"id":bibleBook.id,"title":bibleBook.name,"list":list(bible),"chapter_id":bibleBook.id,"brev":bibleBook.brev,"Currentchapter":chapter}
        # bible.objects.fil
        res.append(Bible_contenu_list)
        # print(res)
    elif fun=="bible_chapter":
        data = request.POST
        bibleBook_model = getattr(models, "sg_bibleBook")
        bibleBook = bibleBook_model.objects.all().values()
        current = data.getlist("current_chapter")
        current_book = bibleBook_model.objects.get(id=current[0])
        bible_model = getattr(models, "sg_bible")
        # nombre_chapitre=bible_model.objects.filter(book__id=current[0]).order_by("-chapitre").first()
        unique_authors = bible_model.objects.filter(book__id=current[0]).values('chapitre').distinct()
        res={"bible":list(bibleBook),"nombre_chapitre":list(unique_authors),"name":current_book.name,"code":current_book.mark}
    elif fun=="messe":
        data = request.POST
        office = commun.Office()
        res = office.lecture(data["date"])
        print(res)
    elif fun=="new_cours_cathegorie":
        data = request.POST
        cathe = models.cathegorie_cours.objects.get(id=data['category_id'])
        cathegories = models.cours.objects.filter(cathegorie=data['category_id'], parent=0).values("id", "title",
                                                                                                  "visuel")
        cathegories = list(cathegories)
        for un in cathegories:
            un["titre"]=un["title"]
            if "https" not in str(un["visuel"]):
                un["visuel"] = "https://www.yzzhenli.org" + str(un["visuel"])
        res = {"titre": cathe.titre, "cathegorie": cathegories}
    return HttpResponse(json.dumps(res, cls=commun.LazyEncoder))
