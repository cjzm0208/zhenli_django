from django.shortcuts import render, HttpResponse
from . import forms
from . import models
import os
from django.shortcuts import redirect
# Create your views here.
import hashlib
import datetime
from django.conf import settings
import json
import time
import ast
from django.db.models import Q
import random
import string
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.core import serializers
import logging
from mutagen.mp3 import MP3
from pydub import AudioSegment
import shutil
from django.db.models import Sum
import ftplib
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import pandas as pd
import ast
from urllib.parse import urlparse
logger = logging.getLogger('django')
import subprocess
from . import commun

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


sidemenus = [{
    'nom': '管理面版',
    'sub_mune': [{
        'nom': '欢迎',
        "url": '/accueil/index/', "show": 'vip',"role":[0,5,10,15]
    }, {
        'nom':'用户',
        "url":'/user/list/0/', "show": 'vip',"role":[0,5,10]
    }, {
        'nom': '分类',
        "url": '/cathegorie/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    }, {
        'nom': '页面',
        "url": '/page/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    }, {
        'nom': '文章',
        "url": '/article/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10,15]
    }, {
        'nom': '课程分类',
        "url": '/cathe_cour/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '课程/听书',
        "url": '/cours/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10,15]
    }, {
        'nom': '圣经',
        "url": '/bible/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '日课',
        "url": '/lecture/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '直播',
        "url": '/live/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '祈祷',
        "url": '/prayer/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '评论',
        "url": '/comment/list/0/?type=article',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '反馈',
        "url": '/feedback/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '设置',
        "url": '/setting/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },{
        'nom': '统计',
        "url": '/statistic/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },
    {
        'nom': 'app首页',
        "url": '/app_index/list/0/',
        'droit': 'vip', "show": 'vip',"role":[0,5,10]
    },
    ]
}]
import pymysql

def table_header(columns, cathe):
    columns1 = '(['
    for column in columns:
        un_column = '{'
        for key, item in column.items():
            if (key == 'formatter'):
                un_column += (''' '%s': %s, ''' % (key, item))
            else:
                un_column += (''' '%s': '%s', ''' % (key, item))
        un_column += '},'
        columns1 += un_column
    columns1 += '])'
    return columns1


def accueil(request, fun):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if (user_info['role'] > 18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'accueil'
    titre = 'Accueils'
    if (fun == "index"):
        pass
        return render(request, "admin/accueil.html", locals())
    elif fun=="modit":
        titre="modit"
        return render(request, "admin/accueil.html", locals())
    elif fun == "modit_js":
        titre="modit_js"
        articles=models.cours.objects.all()
        for un in articles:
            if un.fichier_audio:
                path=un.fichier_audio[1:]
                if os.path.exists(path):
                    try:
                        audio=MP3(path)
                        if audio.info.bitrate<128000:
                            logger.info(path)
                            (src, name) = os.path.split(path)
                            new_path = "static/upload/old/cours/" + name
                            shutil.copy(path, new_path)
                            sound=AudioSegment.from_mp3(new_path)
                            file_handle = sound.export(path, format="mp3",bitrate="128k")
                            audio = MP3(path)
                            models.cours.objects.filter(id=un.id).update(duration=int(audio.info.length))
                    except:
                        logger.error("erreur"+path)
                        # (src, name) = os.path.split(path)
                        # new_path = "static/upload/old/" + name
                        # shutil.copy(path, new_path)
                        # sound=AudioSegment.from_mp3(new_path)
                        # file_handle = sound.export(path, format="mp3",bitrate="128k")
                        # audio = MP3(path)
                        # print(int(audio.info.length))
                        # models.article.objects.filter(id=un.id).update(duration=int(audio.info.length))
        # audio = MP3("static/upload/2022/11/123123123123.mp3")
        # print(audio.info.__dict__)
        # path = "static/upload/2022/11/20221125084210-20210902145907-第1集-天主教會的歷史分期.mp3"
        # (src, name) = os.path.split(path)
        # new_path = "static/upload/old/" + name
        # shutil.copy(path, new_path)
        # sound=AudioSegment.from_mp3(new_path)
        # file_handle = sound.export(path, format="mp3",bitrate="128k")
        # audio = MP3(path)
        # print(audio.info.length)
        return render(request, "admin/accueil.html", locals())
    elif fun=="modi_visuel":
        titre = "modi_visuel"
        data=models.article.objects.order_by("-id").filter(visuel__contains="https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com")
        print(data)
        for un in data:
            visuel1=un.visuel.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com","/static/upload")
            res=models.article.objects.filter(id=un.id).update(visuel=visuel1)
            print(un.id)
        return render(request, "admin/accueil.html", locals())
    elif fun=="modi_user":
        titre = "modi_user"
        models.compte.objects.filter(id=0).delete()
        # data = models.article.objects.filter(fichier_video__isnull=False)
        # res=[]
        # for un in data:
        #     video=un.fichier_video.replace("http://","https://")
        #     models.article.objects.filter(id=un.id).update(fichier_video=video)
            # un.visuel = un.visuel.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com", "/static/upload")
            # res = models.article.objects.filter(id=un.id).update(visuel=un.visuel)
        return render(request, "admin/accueil.html", locals())
    elif fun=="static":
        visits2021 = models.article.objects.filter(date_publier__gte="2021-01-01 00:00:00",date_publier__lte="2021-12-31 23:59:59").aggregate(nums=Sum('lire'))
        visits2022 = models.article.objects.filter(date_publier__gte="2022-01-01 00:00:00",
                                                   date_publier__lte="2022-12-31 23:59:59").aggregate(nums=Sum('lire'))
        # cathes=models.cathegorie.objects.filter()
        # for un in cathes:
        coursvisite2021=models.cours.objects.filter(date_creer__gte="2021-01-01 00:00:00",date_creer__lte="2021-12-31 23:59:59").aggregate(nums=Sum('lire'))
        coursvisite2022 = models.cours.objects.filter(date_creer__gte="2022-01-01 00:00:00",
                                                      date_creer__lte="2022-12-31 23:59:59").aggregate(nums=Sum('lire'))
        res={"2021":visits2021["nums"],"2022":visits2022["nums"],"cours2021":coursvisite2021["nums"],"cours2022":coursvisite2022["nums"]}
        return render(request, "admin/accueil.html", locals())
    # elif fun=="teste_connection":
    #     ftp = ftplib.FTP(timeout=30000)
    #     ftp.connect(host="4o2g2.ftp.infomaniak.com",port=21)
    #     # ftp.set_pasv(False)
    #     # ftp.connect(host=ftp_info.host,port=ftp_info.port)
    #     ftp.login("4o2g2_commun", "communecclesia")
    #     ftp.encoding = "utf-8"
    #     logger.error(ftp)
    #     Welcome = ftp.getwelcome()
    #     logger.error(Welcome)
    #     ftp.cwd("/")
    #     audio_path="static/upload/commun/audio.jpg"
    #     filename="teste1.jpg"
    #     res=0
    #     try:
    #         with open(audio_path, 'rb') as fp:
    #             res = ftp.storbinary("STOR " + filename, fp)
    #             if not res.startswith('226 Transfer complete'):
    #                 logger.error('Upload failed')
    #             fp.close()
    #     except ftplib.all_errors as e:
    #         logger.error('FTP error:', e)
    #         # with open(audio_path, "rb") as file:
    #     #     # try:
    #     #     res=ftp.storbinary(f"STOR {filename}", file, 1024)
    #     #     logger.error(res)
    #     #     res=1
    #     #     # except Exception as e:
    #     #     #     logger.error(e)
    #     #     #     pass
    #     ftp.quit()
    #     return HttpResponse(json.dumps(res))
    elif fun == "delete_old":
        articles=models.article.objects.filter(cathegorie=32,date_creer__lte=datetime.datetime(2022, 1, 1, 12, 30, 0))
        res=[]
        for un in articles:
            if un.fichier_audio:
                path=un.fichier_audio.replace("/static","static")
                if os.path.exists(path):  # 如果文件存在
                    os.remove(path)
                    res.append(un.fichier_audio)
        return render(request, "admin/accueil.html", locals())
    elif fun == "upload_d":
        secret_id = os.getenv('TENCENT_SECRET_ID')  # 替换为用户的 secretId
        secret_key = os.getenv('TENCENT_SECRET_KEY')  # 替换为用户的 secretKey
        region = 'ap-hongkong'  # 替换为用户的 Region
        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)
        # print(client.__dict__)
        response = client.list_buckets(
        )
        directory_path = 'static/wp-content/'
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)  # 你可以在这里添加你需要对文件进行的操作
                response = client.upload_file(
                    Bucket='yzzhenli-1256427631',
                    LocalFilePath=file_path,  # 本地文件的路径
                    Key=file_path,  # 上传到桶之后的文件名
                )
    elif fun == "change_cos":
        values=models.article.objects.filter(fichier_audio__contains="/static/wp-content/")
        res=[]
        for un in values:
            if un.fichier_audio and "https://yzzhenli-1256427631.cos.ap-hongkong" not in un.fichier_audio:
                print(un.id)
                path=un.fichier_audio.replace("/static/wp-content/","https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com/static/wp-content/")
                # path = un.contenu.replace("http://www.yzzhenli.orghttps://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com",
                #                          "https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com")
                res.append([un.id])
                models.article.objects.filter(id=un.id).update(fichier_audio=path)
        return render(request, "admin/accueil.html", locals())
    elif fun == "read_json":
        # 打开json文件，使用utf-8编码
        with open('index/index_lectures.json', 'r', encoding='utf-8') as f:
            # 使用json.load()方法将文件内容转换为Python字典
            data = json.load(f)
            # 打印转换后的字典
            for un in data:
                if un["type"] == "table":
                    for une in un["data"]:
                        print(une)
                        models.sg_lecture.objects.create(id=une["id"], impair=une["impair"], abc=une["abc"], fete=une["fete"], sign=une["signe"], name=une["nom_jour1"])
    elif fun == "zhangjie":
        books=models.sg_bibleBook.objects.all()
        for un in books:
            chapitre=models.sg_bible.objects.filter(book=un.id).values("chapitre").distinct()
            new_cha=[]
            for une in chapitre:
                new_cha.append(une["chapitre"])
            models.sg_bibleBook.objects.filter(id=un.id).update(chapitre=json.dumps(new_cha))
    elif fun=="wenwen":
        df = pd.read_excel('cache/cath.xlsx', sheet_name='Sheet1')
        header = df.columns.tolist()  # 标题行
        rows_list = [header] + df.values.tolist()  # 合并标题和数据

        # 打印结果
        print(rows_list)
        # wewens=models.article.objects.filter(cathegorie=30)
        # res=[]
        # for un in wewens:
        #     res.append([un.id,un.title])
    elif fun=="shengyue":
        cath=[53]
        caths=models.cathegorie.objects.filter(parent=53)
        for un in caths:
            cath.append(un.id)
        articles=models.article.objects.filter(cathegorie__in=cath)
        res=[]
        for un in articles:
            date=un.date_motifier.strftime("%m-%d")
            models.article.objects.filter(id=un.id).update(frequency_date=date)
    elif fun == "vod":
        old_text="/static/upload/2024/"
        new_text="https://cdn.yzzhenli.com/2024/"
        # old_text= "https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com/"
        # new_text = "https://cdn.yzzhenli.com/"
        res = []
        articles=models.article.objects.filter(visuel__icontains=old_text)
        for un in articles:
            val=["visuel",un.id,un.visuel]
            if un.visuel:
                visuel=un.visuel.replace(old_text,new_text)
                val.append(visuel)
                res.append(val)
                models.article.objects.filter(id=un.id).update(visuel=visuel)
        articles=models.article.objects.filter(fichier_audio__icontains=old_text)
        for un in articles:
            val_fichier_audio=["fichier_audio",un.id,un.fichier_audio]
            if un.fichier_audio:
                fichier_audio=un.fichier_audio.replace(old_text,new_text)
                val_fichier_audio.append(fichier_audio)
                res.append(val_fichier_audio)
                models.article.objects.filter(id=un.id).update(fichier_audio=fichier_audio)
        articles=models.article.objects.filter(contenu__icontains=old_text)
        for un in articles:
            val_contenu=["contenu",un.id,un.contenu[:100]]
            if un.contenu:
                contenu=un.contenu.replace(old_text,new_text)
                val_contenu.append(contenu[:100])
                res.append(val_contenu)
                models.article.objects.filter(id=un.id).update(contenu=contenu)
        cours=models.cours.objects.filter(visuel__icontains=old_text)
        for un in cours:
            val_cours=["cours_visuel",un.id,un.visuel]
            if un.visuel:
                cours_visuel=un.visuel.replace(old_text,new_text)
                val_cours.append(cours_visuel)
                res.append(val_cours)
                models.cours.objects.filter(id=un.id).update(visuel=cours_visuel)
        cours = models.cours.objects.filter(fichier_audio__icontains=old_text)
        for un in cours:
            val_cours_fichier_audio=["cours_fichier_audio",un.id,un.fichier_audio]
            if un.fichier_audio:
                fichier_audio_cours=un.fichier_audio.replace(old_text,new_text)
                val_cours_fichier_audio.append(fichier_audio_cours)
                res.append(val_cours_fichier_audio)
                models.cours.objects.filter(id=un.id).update(fichier_audio=fichier_audio_cours)
        cours=models.cours.objects.filter(contenu__icontains=old_text)
        for un in cours:
            val_cours_contenu=["cours_contenu",un.id,un.contenu[:100]]
            if un.contenu:
                contenu_cours=un.contenu.replace(old_text,new_text)
                val_cours_contenu.append(contenu_cours[:100])
                res.append(val_cours_contenu)
                models.cours.objects.filter(id=un.id).update(contenu=contenu_cours)
    elif fun =="jiucuo":
        res=[]
        cours=models.cours.objects.filter(fichier_audio__icontains="[")
        for un in cours:
            val=[un.id,un.fichier_audio]
            fichier_audio_list=ast.literal_eval(un.fichier_audio)
            val.append(fichier_audio_list[2])
            res.append(val)
            # models.cours.objects.filter(id=un.id).update(fichier_audio=fichier_audio_list[2])
    elif fun == "video":
        pass
        res = []
        # articles=models.article.objects.filter(fichier_video__isnull=False)
        # for un in articles:
        #     filename4, extension = os.path.splitext(os.path.basename(urlparse(un.fichier_video).path))
        #     new_ficher_video=f"https://cdn.yzzhenli.com/video/{filename4}/hls/master.m3u8"
        #     res.append({"id":un.id,"cathe":"article","old":un.fichier_video,"new":new_ficher_video})
        #     models.article.objects.filter(id=un.id).update(fichier_video=new_ficher_video)
        # cours=models.cours.objects.filter(fichier_video__isnull=False)
        # for un in cours:
        #     filename4, extension = os.path.splitext(os.path.basename(urlparse(un.fichier_video).path))
        #     new_ficher_video = f"https://cdn.yzzhenli.com/video/{filename4}/hls/master.m3u8"
        #     res.append({"id":un.id,"cathe":"cours","old": un.fichier_video,"new":new_ficher_video})
        #     models.cours.objects.filter(id=un.id).update(fichier_video=new_ficher_video)
    elif fun == "duraiton":
        # print(1232)
        # url="https://cdn.yzzhenli.com/2026/01/20260129205349-bddac7d5.mp3"
        # B2=commun.B2()
        # temp_download=B2.download_and_convert_audio(url)
        # print(temp_download)
        # new_url=url.replace("https://cdn.yzzhenli.com/","").replace(".mp3","_128k.mp3")
        # res=B2.upload_to_b2(temp_download,new_url)
        # print(res)
        # if os.path.exists(temp_download):
        #     os.remove(temp_download)
        audios=models.cours.objects.filter(fichier_audio__isnull=False)
        print(audios)
        res=[]
        for un in audios:
            if un.fichier_audio and "_128k" not in un.fichier_audio:
                try:
                    url=un.fichier_audio
                    B2 = commun.B2()
                    temp_download = B2.download_and_convert_audio(url)
                    new_url = url.replace("https://cdn.yzzhenli.com/", "").replace(".mp3", "_128k.mp3")
                    new_ficher_audio = B2.upload_to_b2(temp_download, new_url)
                    print([un.id,un.title,un.fichier_audio,new_ficher_audio])
                    res.append([un.id,un.title,un.fichier_audio,new_ficher_audio])
                    models.cours.objects.filter(id=un.id).update(fichier_audio=new_ficher_audio)
                    if os.path.exists(temp_download):
                        os.remove(temp_download)
                except:
                    pass
    return render(request, "admin/accueil.html", locals())


def get_duration(url):
    """获取单个 URL 的音频时长"""
    command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        url
    ]

    try:
        # 执行命令
        result = subprocess.check_output(command, text=True).strip()
        return float(result)
    except Exception as e:
        print(f"解析失败: {url} | 错误: {e}")
        return None

def user(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'user'
    titre = '用户'
    les_class = {
        'email': [True, 'col', False],
        'prenom': [False, 'col', True],
        'role': [True, 'col', False],
        'sex': [False, 'col', True],
        'naissance': [True, 'col', False],
        'Tel': [False, 'col', True],
        'pays': [True, 'col', False],
        'ville': [False, 'col', True],
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'maison': [False, 'col hide', False],
        'responsable': [False, 'col hide', False],
    }
    hide_lable = {'user_id': False,
                  'user_name': False,
                  }
    special = {
        'role': 'role_input'
    }
    if (fun == "list"):
        if user_info['role']==0:
            choix = {
                0: "全局管理员",
                5: "管理员",
                10: "负责人",
                15: "老师",
                20: "订阅者",
                25:"被屏蔽",
            }
        elif user_info['role']==5 or user_info['role']==10:
            choix = {
                15: "老师",
                20: "订阅者",
                25: "被屏蔽",
            }
        columns = [{
            'field': 'id',
            'title': 'ID',
            'sortable': True,
        }, {
            'field': 'email',
            'title': '邮箱',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                return '<a href="/''' + cathe + '''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        }, {
            'field': 'prenom',
            'title': '姓名',
            'sortable': True,
        },{
            'field': 'role',
            'title': '权限',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                        return choix[value]
                        }'''
        },{
            'field': 'date_motifier',
            'title': '修改日期',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.compte.objects.order_by('-id').filter(role__gte=user_info['role']).values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        choix = json.dumps(choix, cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif(fun=="edit_form"):
        vaules = models.compte.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.moncompte(instance=vaules, user_info=user_info)
        else:
            data=request.POST
            data=data.copy()
            if(int(data['role'])<int(user_info['role'])):
                return render(request, "admin/faute_sans_droit.html", locals())
            les_forms = models.moncompte(instance=vaules, data=data, user_info=user_info)
            if les_forms.is_valid():  # 验证
                les_forms.save()  # 保存
                return redirect('/' + cathe+'/list/0')  # 成功跳转
        return render(request, "admin/form.html", locals())
    elif fun=='delete':
        if (user_info['role'] != 0):
            return render(request, "admin/faute_sans_droit.html", locals())
        models.quotidien.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转
    elif fun=='importe':
        # 打开数据库连接
        db = pymysql.connect("150.109.37.53", "yzzhenli", "Jesus1225", "yzzhenli")
        cursor = db.cursor()
        # SQL 查询语句
        sql = "SELECT * FROM wp_posts WHERE ID > 25218 AND post_status='publish' AND post_type='post'"
        # sql = "SELECT * FROM wp_posts WHERE ID = 21971"
        #12295 12532 12556 23 15000-15769 16590 16610
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for un in results:
            data = {}
            print(un[0])
            data['title'] = un[5]
            visule=chercher_visuel(un[0], cursor)
            data['visuel']=visule
            cathes=chercher_cathegorie(un[0], cursor)
            data['cathegorie']=cathes
            data['lire'] = chercher_lire(un[0], cursor)
            contenu=video_audio(un[4])
            if(contenu[0]=='audio'):
                data['fichier_audio']=contenu[1]
                data['contenu']=contenu[2]
            elif(contenu[0]=='video'):
                data['fichier_video'] = contenu[1]
                data['contenu'] = contenu[2]
            else:
                data['contenu'] = contenu[1]
            data['user_id']=user_info['id']
            data['user_name']='真理文化'
            data['observation']=1
            print(data)
            les_forms = models.article_input(data=data, user_info=user_info)
            print(les_forms.errors)
            if les_forms.is_valid():
                res=les_forms.save()
                models.article.objects.filter(id=res.id).update(date_motifier=un[2], date_creer=un[2])
        return render(request, "admin/1.html", locals())
from phpserialize import serialize, unserialize
import pickle
def chercher_visuel(id,cursor):
    sql = "SELECT * FROM wp_postmeta WHERE post_id = "+str(id)+" AND meta_key='_thumbnail_id'"
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchone()
    if not results:
        return ''
    sql = "SELECT * FROM wp_postmeta WHERE post_id = " + results[3]
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    if not results:
        return ''
    for un in results:
        if un[2]=='_wp_attached_file':
            src=un[3]
    for un in results:
        if un[2]=='_wp_attachment_metadata':
            # binary_data = bytes(un[3], 'utf-8')
            binary_data = un[3].encode('utf-8')
            output=unserialize(binary_data)
            output = {
                key.decode(): val.decode() if isinstance(val, bytes) else val
                for key, val in output.items()
            }
            if 'sizes' not in output:
                return ''
            output=output['sizes']
            output = {
                key.decode(): val.decode() if isinstance(val, bytes) else val
                for key, val in output.items()
            }
            if 'thumbnail' not in output:
                return ''
            output = output['thumbnail']
            output = {
                key.decode(): val.decode() if isinstance(val, bytes) else val
                for key, val in output.items()
            }
            src_arr=src.split('/')
            return '/static/wp-content/uploads/'+src_arr[0]+'/'+src_arr[1]+'/'+output['file']

def chercher_cathegorie(id,cursor):
    single=[47,49,50,51,53,54,58,91,96]
    sql = "SELECT * FROM wp_term_relationships WHERE object_id = " + str(id)
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    res=[]
    for un in results:
        if un[1] not in single:
            if models.cathegorie.objects.filter(original=un[1]).exists():
                cathe=models.cathegorie.objects.get(original=un[1])
                res.append(cathe.id)
    return res
def video_audio(contenu):
    if '[/audio]' in contenu and '[audio wav' not in contenu and '[audio m4a' not in contenu:
        a = r'\[audio mp3=\"(.*?)"\]\[\/audio\]'
        audios = re.findall(a, contenu)
        print(contenu)
        contenu = contenu.replace('[audio mp3="' + audios[0] + '"][/audio]', '')
        contenu = contenu.replace('<p></p>', '')
        contenu = contenu.replace('/wp-content/uploads/', '/static/wp-content/uploads/')
        return ['audio','/static'+audios[0],contenu]
    elif '[/audio]' in contenu and '[audio wav' in contenu:
        print(1231231)
        a = r'\[audio wav=\"(.*?)"\]\[\/audio\]'
        audios = re.findall(a, contenu)
        contenu = contenu.replace('[audio wav="' + audios[0] + '"][/audio]', '')
        contenu = contenu.replace('<p></p>', '')
        contenu = contenu.replace('/wp-content/uploads/', '/static/wp-content/uploads/')
        return ['audio', '/static' + audios[0], contenu]
    elif '[/audio]' in contenu and '[audio m4a' in contenu:
        a = r'\[audio m4a=\"(.*?)"\]\[\/audio\]'
        audios = re.findall(a, contenu)
        contenu = contenu.replace('[audio m4a="' + audios[0] + '"][/audio]', '')
        contenu = contenu.replace('<p></p>', '')
        contenu = contenu.replace('/wp-content/uploads/', '/static/wp-content/uploads/')
        return ['audio', '/static' + audios[0], contenu]
    elif '[/embed]' in contenu:
        a = r'\[embed\](.*?)\[\/embed\]'
        videos = re.findall(a, contenu)
        contenu=contenu.replace('[embed]'+videos[0]+'[/embed]','')
        contenu=contenu.replace('<p></p>','')
        contenu = contenu.replace('/wp-content/uploads/', '/static/wp-content/uploads/')
        return ['video',videos[0],contenu]
    else:
        return ['',contenu]
def chercher_lire(id,cursor):
    sql = "SELECT * FROM wp_top_ten WHERE postnumber = " + str(id)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results[1]:
        return results[1]
    else:
        return 0

def cathegorie(request,fun,num):
    if not request.session.get('is_login', None):
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'cathegorie'
    titre = '分类'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'maison_name': [False, 'col', False],
        'maison': [False, 'col', False],
    }
    tag_special = {
        'visuel': 'button_visuel',
    }
    droit = ['observation','date_limit','visuel']
    if (fun == "list"):
        columns = [{
            'field': 'titre',
            'title': '名称',
            'sortable': True,
            'formatter':'''function (value, row, index) {
                return '<a href="/'''+cathe+'''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        },{
            'field': 'parent',
            'title': '父分类',
            'sortable': True,
        },{
            'field': 'ordre',
            'title': '顺序',
            'sortable': True,
        },{
            'field': 'date_motifier',
            'title': '修改时间',
            'sortable': True,
        },{
            'field': 'user_name',
            'title': '修改人',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.cathegorie.objects.order_by('-id').all().values(*value_list)
        for un in datas:
            print(un)
            if models.cathegorie.objects.filter(id=un["parent"]).exists():
                cathegorie=models.cathegorie.objects.get(id=un["parent"])
                un["parent"]=cathegorie.titre
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules=''
            les_forms = models.cathegorie_input(user_info=user_info)
        else:
            les_forms = models.cathegorie_input(data=request.POST,user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.cathegorie.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.cathegorie_input(instance=vaules,user_info=user_info)
        else:
            les_forms = models.cathegorie_input(instance=vaules, data=request.POST,user_info=user_info)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/'+ cathe+'/list/0')  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.cathegorie.objects.get(id=num)
        models.cathegorie.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转

def page(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'page'
    titre = 'Pages'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'maison_name': [False, 'col', False],
        'maison': [False, 'col', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
    }
    droit = ['observation']
    if (fun == "list"):
        columns = [{
            'field': 'title',
            'title': 'Titre',
            'sortable': True,
            'formatter':'''function (value, row, index) {
                return '<a href="/'''+cathe+'''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        },{
            'field': 'date_motifier',
            'title': 'Modifié le',
            'sortable': True,
        },{
            'field': 'user_name',
            'title': 'Par',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.pages.objects.order_by('-id').all().values(*value_list)
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules=''
            les_forms = models.pages_input(user_info=user_info)
        else:
            les_forms = models.pages_input(data=request.POST,user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.pages.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.pages_input(instance=vaules,user_info=user_info)
        else:
            les_forms = models.pages_input(instance=vaules, data=request.POST,user_info=user_info)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/'+ cathe+'/list/0')  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.pages.objects.get(id=num)
        if vaules.maison != user_info['maison']:
            return render(request, "admin/faute_sans_droit.html", locals())
        models.pages.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转

def article(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'article'
    titre = '文章'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','date_motifier',"frequency_date"]
    cathegories = models.cathegorie.objects.order_by('ordre', 'id').exclude(id=0)
    new_cathegories=[]
    for un in cathegories:
        if un.parent == 0:
            class1={"id":un.id,"titre":un.titre,"sub_cathegories":[]}
            for un1 in cathegories:
                if un1.parent==un.id:
                    class2={"id":un1.id,"titre":un1.titre,"sub_cathegories":[]}
                    for un2 in cathegories:
                        if un2.parent==un1.id:
                            class3={"id":un2.id,"titre":un2.titre}
                            class2["sub_cathegories"].append(class3)
                    class1["sub_cathegories"].append(class2)
            new_cathegories.append(class1)
    if (fun == "list"):
        columns = [{
            'field': 'title',
            'title': '标题',
            'sortable': True,
            'formatter':'''function (value, row, index) {
                return '<a target="_blank" href="/'''+cathe+'''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        },{
            'field': 'cathegorie',
            'title': '分类',
            'sortable': True,
            'formatter':'fun_choix'
        },{
            'field': 'date_motifier',
            'title': '发布时间',
            'sortable': True,
        },{
            'field': 'user_name',
            'title': '用户名',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        get = request.GET
        if user_info['role'] > 11:
            filter = {"user_id": user_info['id']}
        else:
            filter = {}
        data_search={}
        if('search' in get):
            filter['title__contains']=get['search']
            data_search['Chercher']=get['search']
        if ('cathegory' in get):
            cathegory=models.cathegorie.objects.get(id=get['cathegory'])
            new_cathegory = [get['cathegory']]
            data_search['cathegory'] = get['cathegory']
            if cathegory.parent==0:
                cathegorys=models.cathegorie.objects.filter(parent=get['cathegory'])
                for un in cathegorys:
                    new_cathegory.append(un.id)
            filter['cathegorie__in']=new_cathegory
        if('order' in get):
            datas = models.article.objects.order_by(get['order']).filter(**filter).distinct()
        else:
            datas = models.article.objects.order_by('-id').filter(**filter).distinct()
        p = Paginator(datas, 20)
        if ('page' in get):
            page_num = get['page']
        else:
            page_num = 1
        page = p.page(page_num)
        list_data=serializers.serialize('json',page, fields=('id','title','user_name','date_motifier','cathegorie'))
        cathegories=models.cathegorie.objects.all()
        choix=models.cathegorie.objects.all().values_list('id','titre')
        choix=json.dumps(list(choix))
        #tabbar de list
        chercher=forms.ListChercher(data=data_search)
        comments=True
        return render(request, "admin/liste_page.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules=''
            les_forms = models.article_input(user_info=user_info)
        else:
            data=request.POST
            data=data.copy()
            data["new_cotenu"]=json.dumps([])
            les_forms = models.article_input(data=data,user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.article.objects.get(id=num)
        categories_checked = vaules.cathegorie.all()
        print(categories_checked)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.article_input(instance=vaules,user_info=user_info)
        else:
            print(request.POST)
            les_forms = models.article_input(instance=vaules, data=request.POST,user_info=user_info)
            if les_forms.is_valid():  # 验证
                les_forms.save()
                return redirect('/' + cathe + '/list/0')  # 成功跳转
            else:
                logger.error(les_forms.errors)
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.article.objects.get(id=num)
        models.article.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转
    elif fun=='data':
        article=models.article.objects.filter(id__gt=5790)
        db = pymysql.connect("150.109.37.53", "yzzhenli", "Jesus1225", "yzzhenli")
        cursor = db.cursor()
        # SQL 查询语句
        for un in article:
            if un.title:
                sql = "SELECT * FROM wp_posts WHERE post_title = '"+un.title+"'"
                cursor.execute(sql)
                results = cursor.fetchone()
                if results:
                    print(un.id,results[0])
                    models.article.objects.filter(id=un.id).update(date_motifier=results[2],date_creer=results[2])
        return render(request, "admin/1.html", locals())
    elif fun=='deletes':
        models.article.objects.filter(id__gt=5790).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转
    elif fun=='xiugai':
        all=models.article.objects.filter(id=73)
        for un in all:
            models.article.objects.filter(id=un.id).update(date_publier=un.date_motifier)
        return redirect('/' + cathe + '/list/0')  # 成功跳转

def cours(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'cours'
    titre = '文章'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False,
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
        'parent': [False, 'col hide_input', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','cathegorie']
    parent=0
    get=request.GET
    print(get)
    if 'parent' in get:
        parent=int(get['parent'])
    ajouter_suffix='&parent='+str(parent)
    if (fun == "list"):
        columns = [{
            'field': 'title',
            'title': '名称',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                return '<a href="/''' + cathe + '''/edit_form/'+row.id+'/?parent=''' + str(parent) + '''">'+value+'</a>'
                }'''
        },{
            'field': 'cathegorie__titre',
            'title': '分类',
            'sortable': True,
        },{
            'field': 'ordre',
            'title': '顺序',
            'sortable': True,
        }, {
            'field': 'date_motifier',
            'title': '修改日期',
            'sortable': True,
        }, {
            'field': 'user_name',
            'title': '修改人',
            'sortable': True,
        }]
        if parent==0:
            columns.insert(1,{
            'field': 'title',
            'title': '文章列表',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                return '<a href="/''' + cathe + '''/list/0/?parent='+row.id+'">文章列表</a>'
                }'''
        })
        value_list = ['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        if user_info['role'] > 11:
            datas = models.cours.objects.order_by('ordre','-id').filter(parent=parent,user_id=user_info['id']).values(*value_list)
        else:
            datas = models.cours.objects.order_by('ordre','-id').filter(parent=parent).values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        comments = True
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules = ''
            les_forms = models.cours_input(user_info=user_info)
        else:
            data = request.POST
            data=data.copy()
            data['parent']=parent
            les_forms = models.cours_input(data=data, user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/' + cathe + '/list/0/?'+ajouter_suffix)
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.cours.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.cours_input(instance=vaules, user_info=user_info)
        else:
            data = request.POST
            les_forms = models.cours_input(instance=vaules, data=data, user_info=user_info)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/' + cathe + '/list/0/?'+ajouter_suffix)  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun == 'delete':
        vaules = models.cours.objects.get(id=num)
        models.cours.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转
    elif fun=='comments':
        columns = [{
            'field': 'parent__title',
            'title': '文章',
            'sortable': True,
        }, {
            'field': 'contenu',
            'title': '内容',
            'sortable': True,
        }, {
            'field': 'user_id__prenom',
            'title': '用户名',
            'sortable': True,
        }, {
            'field': 'user_id__prenom',
            'title': '回复',
            'sortable': True,
        }, {
            'field': 'date_creer',
            'title': '创建日期',
            'sortable': True,
        }]
        value_list = ['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.comments_cours.objects.order_by('-id').all().values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        return render(request, "admin/liste.html", locals())

def live(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'live'
    titre = '直播'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
    }
    tag_special = {
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','start','end','professeur']
    if (fun == "list"):
        columns = [{
            'field': 'title',
            'title': '标题',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                        return '<a href="/''' + cathe + '''/edit_form/'+row.id+'">'+value+'</a>'
                        }'''
        }, {
            'field': 'start',
            'title': '开始时间',
            'sortable': True,
        }, {
            'field': 'end',
            'title': '结束时间',
            'sortable': True,
        }, {
            'field': 'date_motifier',
            'title': '修改时间',
            'sortable': True,
        }, {
            'field': 'user_name',
            'title': '用户名',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.live.objects.order_by('-id').all().values(*value_list)
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            les_forms = models.live_input(user_info=user_info)
        else:
            les_forms = models.live_input(data=request.POST,user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.live.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.live_input(instance=vaules,user_info=user_info)
        else:
            les_forms = models.live_input(instance=vaules, data=request.POST,user_info=user_info)
            if les_forms.is_valid():  # 验证
                les_forms.save()
                return redirect('/' + cathe + '/list/0')  # 成功跳转
            else:
                logger(les_forms.errors)
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.live.objects.get(id=num)
        models.live.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转

def feedback(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'feedback'
    titre = '反馈'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
    }
    tag_special = {
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','start','end','professeur']
    if (fun == "list"):
        columns = [{
            'field': 'email',
            'title': '邮箱',
            'sortable': True,
        },{
            'field': 'contenu',
            'title': '反馈内容',
            'sortable': True,
        },{
            'field': 'parent',
            'title': '回复',
            'sortable': True,
            'formatter': '''feedback_reponse'''
        },{
            'field': 'date_motifier',
            'title': '修改时间',
            'sortable': True,
        }, {
            'field': 'user_name',
            'title': '用户名',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.feedback.objects.order_by('-id').all().values(*value_list)
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        get=request.GET
        if request.method != 'POST':
            value = models.feedback.objects.get(id=get['parent'])
            les_forms = models.feedback_input(
                initial={"user_id": user_info['id'], 'parent': get['parent'],"user_name": user_info['nom']})
        else:
            les_forms = models.feedback_input(data=request.POST)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0/')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.feedback.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.feedback_input(instance=vaules)
        else:
            data = request.POST
            les_forms = models.feedback_input(instance=vaules, data=data)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/' + cathe + '/list/0/')  # 成功跳转
        return render(request, "admin/form2.html", locals())


def comment(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'comment'
    titre = '文章'
    hide_lable = {'user_id': False,
                  'parent': False,
                  'parent_comment': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','date_motifier']
    get = request.GET
    if fun=='list':
        columns = [{
            'field': 'title',
            'title': '文章',
            'sortable': True,
            'formatter': '''list_comment'''
        }, {
            'field': 'contenu',
            'title': '内容',
            'sortable': True,
        }, {
            'field': 'type',
            'title': '类型',
            'sortable': True,
            'formatter': '''list_type_comment'''
        },{
            'field': 'user_id__prenom',
            'title': '回复',
            'sortable': True,
            'formatter': '''list_reponse'''
        },{
            'field': 'user_id__prenom',
            'title': '用户名',
            'sortable': True,
        }, {
            'field': 'date_creer',
            'title': '创建日期',
            'sortable': True,
        }]
        value_list = ['id','parent_comment']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.comments.objects.order_by('-id').all().values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        ajouter_suffix="type="+get['type']
        if request.method != 'POST':
            value = models.comments.objects.get(id=get['parent'])
            les_forms = models.comments_input(
                initial={"user_id": user_info['id'], 'parent': value.parent, 'parent_comment': get['parent'],'title':value.title,'type':value.type})
        else:
            les_forms = models.comments_input(data=request.POST)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0/?type='+get['type'])
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        values = models.comments.objects.get(id=num)
        if values.type=="article":
            value_article=models.article.objects.get(id=values.parent)
        else:
            value_article = models.cours.objects.get(id=values.parent)
        if values.parent_comment:
            value=models.comments.objects.get(id=values.parent_comment)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.comments_input(instance=values)
        else:
            les_forms = models.comments_input(instance=values, data=request.POST)
            if les_forms.is_valid():  # 验证
                les_forms.save()
                return redirect('/'+ cathe+'/list/0/?type='+get['type'])  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.comments.objects.get(id=num)
        models.comments.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0/')

def setting(request,fun,key):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'setting'
    titre = '设置'
    dossiers=['index_image_logo','index_left_1','index_middle']
    if (fun == "list"):
        if request.method != 'POST':
            values_setting=models.setting.objects.all()
            ini={}
            for un in values_setting:
                if un.key=="zhuda_cathe":
                    ini[un.key] = json.loads(un.contenu)
                else:
                    ini[un.key]=un.contenu
            settings_form=forms.settingForm(initial=ini)
        else:
            data=request.POST
            data=data.copy()
            data["zhuda_cathe"]=json.dumps(data.getlist("zhuda_cathe"))
            settings_form = forms.settingForm(initial=data)
            del data['csrfmiddlewaretoken']
            for key in data:
                if models.setting.objects.filter(key=key).exists():
                    models.setting.objects.filter(key=key).update(contenu=data[key],date_motifier=datetime.datetime.now())
                else:
                    models.setting.objects.create(key=key,contenu=data[key])
            return redirect('/setting/list/0/')
        return render(request, "admin/setting_list.html", locals())



def statistic(request,fun,key):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'statistic'
    titre = '统计'
    dossiers=['index_image_logo','index_left_1','index_middle']
    # date_start=datetime.datetime.date()
    # date_end=date_start+datetime.timedelta(days=7)
    date_time_start_str = "2025-01-01 00:00:00"
    date_start = datetime.datetime.strptime(date_time_start_str, "%Y-%m-%d %H:%M:%S")
    date_time_end_str = "2025-10-01 00:00:00"
    date_end = datetime.datetime.strptime(date_time_end_str, "%Y-%m-%d %H:%M:%S")
    result_a = models.article.objects.filter(date_publier__lte=date_end,date_publier__gte=date_start).aggregate(total_sum=Sum('lire'))['total_sum']
    cathegory=models.cathegorie.objects.filter(parent=0)
    res_c=[]
    for un in cathegory:
        new_cathegory=[un.id]
        cathegorys = models.cathegorie.objects.filter(parent=un.id)
        for une in cathegorys:
            new_cathegory.append(une.id)
        print(models.article.objects.filter(cathegorie__in=new_cathegory,date_publier__lte=date_end,date_publier__gte=date_start))
        result_c=models.article.objects.filter(date_publier__lte=date_end,date_publier__gte=date_start,cathegorie__in=new_cathegory).aggregate(total_sum=Sum('lire'))['total_sum']
        res_c.append({"titre":un.titre,"sum":result_c})
    print(res_c)
    result_k = models.cours.objects.filter(date_creer__lte=date_end, date_creer__gte=date_start).aggregate(
        total_sum=Sum('lire'))['total_sum']
    return render(request, "admin/statistic.html", locals())

def cathe_cours(request,fun,num):
    if not request.session.get('is_login', None):
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'cathe_cour'
    titre = '分类'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'maison_name': [False, 'col', False],
        'maison': [False, 'col', False],
    }
    tag_special = {
        'visuel': 'button_visuel',
    }
    droit = ['observation','date_limit','visuel']
    if (fun == "list"):
        columns = [{
            'field': 'titre',
            'title': '名称',
            'sortable': True,
            'formatter':'''function (value, row, index) {
                return '<a href="/'''+cathe+'''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        },{
            'field': 'parent__titre',
            'title': '父分类',
            'sortable': True,
        },{
            'field': 'ordre',
            'title': '顺序',
            'sortable': True,
        },{
            'field': 'date_motifier',
            'title': '修改时间',
            'sortable': True,
        },{
            'field': 'user_name',
            'title': '修改人',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.cathegorie_cours.objects.order_by('-id').all()[:100].values(*value_list)
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules=''
            les_forms = models.cathegorie_cours_input(user_info=user_info)
        else:
            les_forms = models.cathegorie_cours_input(data=request.POST,user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.cathegorie_cours.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.cathegorie_cours_input(instance=vaules,user_info=user_info)
        else:
            les_forms = models.cathegorie_cours_input(instance=vaules, data=request.POST,user_info=user_info)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/'+ cathe+'/list/0')  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.cathegorie_cours.objects.get(id=num)
        models.cathegorie_cours.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转

def bible(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'bible'
    titre = '圣经'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False,
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
        'parent': [False, 'col hide_input', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','cathegorie']
    parent=0
    get=request.GET
    print(get)
    if 'parent' in get:
        parent=int(get['parent'])
    ajouter_suffix='&parent='+str(parent)
    if (fun == "list"):
        columns = [{
            'field': 'name',
            'title': '名称',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                return '<a href="/''' + cathe + '''/edit_form/'+row.id+'/?parent=''' + str(parent) + '''">'+value+'</a>'
                }'''
        },{
            'field': 'chapitre',
            'title': '章节列表',
            'sortable': True,
            'formatter': 'chapitre_list'
        },{
            'field': 'brev',
            'title': '简写',
            'sortable': True,
        },{
            'field': 'mark',
            'title': '标记',
            'sortable': True,
        }]
        value_list = ['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.sg_bibleBook.objects.order_by('id').values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        comments = True
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules = ''
            les_forms = models.sg_bibleBook_input()
        else:
            data = request.POST
            data=data.copy()
            data['parent']=parent
            les_forms = models.sg_bibleBook_input(data=data)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/' + cathe + '/list/0/?'+ajouter_suffix)
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.sg_bibleBook.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.sg_bibleBook_input(instance=vaules, )
        else:
            data = request.POST
            les_forms = models.sg_bibleBook_input(instance=vaules, data=data)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/' + cathe + '/list/0/?'+ajouter_suffix)  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun == 'delete':
        vaules = models.sg_bibleBook.objects.get(id=num)
        models.sg_bibleBook.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转
    if (fun == "chapitre"):
        get=request.GET
        columns = [{
            'field': 'book__brev',
            'title': '书',
            'sortable': True,
        },{
            'field': 'chapitre',
            'title': '章',
            'sortable': True,
        },{
            'field': 'partie',
            'title': '节',
            'sortable': True,
        },{
            'field': 'contenu',
            'title': '内容',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                        return '<a href="/''' + cathe + '''/verse/'+row.id+'/?book=''' + str(get["book"]) + '''&chapitre='''+str(num)+'''">'+value+'</a>'
                        }'''
        }]
        value_list = ['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.sg_bible.objects.order_by('id').filter(chapitre=num,book=get["book"]).values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        comments = True
        return render(request, "admin/liste.html", locals())
    elif (fun == "verse"):
        get = request.GET
        print(123)
        print(get)
        vaules = models.sg_bible.objects.get(id=num)
        ajouter_suffix = '''book=''' + str(get["book"]) + '''&chapitre='''+str(get["chapitre"])
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.sg_bible_input(instance=vaules, )
        else:
            data = request.POST
            les_forms = models.sg_bible_input(instance=vaules, data=data)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                print('/' + cathe + '/chapitre/'+get["chapitre"]+'/?book='+get["book"])
                return redirect('/' + cathe + '/chapitre/'+get["chapitre"]+'/?book='+get["book"])  # 成功跳转
        return render(request, "admin/form2.html", locals())


def lecture(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role']>11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'lecture'
    titre = '日课'
    hide_lable = {'user_id': False,
                  'parent': False,
                  'parent_comment': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'lire': [False, 'col hide_input', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','date_motifier']
    get = request.GET
    if fun=='list':
        columns = [{
            'field': 'impair',
            'title': '单双年',
            'sortable': True,
            'formatter':"fun_lecture_impair"
        }, {
            'field': 'abc',
            'title': '甲乙丙',
            'sortable': True,
            'formatter': "fun_lecture_abc"
        }, {
            'field': 'name',
            'title': '名称',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                        return '<a href="/''' + cathe + '''/edit_form/'+row.id+'/">'+value+'</a>'
                        }'''
        },{
            'field': 'fete',
            'title': '节庆日',
            'sortable': True,
            'formatter': "fun_lecture_fete"
        },{
            'field': 'sign',
            'title': '标记',
        }]
        value_list = ['id']
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.sg_lecture.objects.order_by('-id').all().values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        ajouter_suffix="type="+get['type']
        if request.method != 'POST':
            value = models.comments.objects.get(id=get['parent'])
            les_forms = models.comments_input(
                initial={"user_id": user_info['id'], 'parent': value.parent, 'parent_comment': get['parent'],'title':value.title,'type':value.type})
        else:
            les_forms = models.comments_input(data=request.POST)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/'+ cathe+'/list/0/?type='+get['type'])
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.sg_lecture.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.sg_lecture_input(instance=vaules)
        else:
            data = request.POST
            print(data)
            les_forms = models.sg_lecture_input(instance=vaules, data=data)
            print(les_forms.errors)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/' + cathe + '/list/0/')  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun=='delete':
        vaules = models.comments.objects.get(id=num)
        models.comments.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0/')


def prayer(request,fun,num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if(user_info['role']>18):
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'prayer'
    titre = '祈祷'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
    }
    tag_special = {
        'visuel': 'button_visuel',
    }
    droit = ['observation','visuel','start','end','professeur']
    if (fun == "list"):
        columns = [{
            'field': 'id',
            'title': '邮箱',
            'sortable': True,
            "formatter":"fun_prayer"
        },{
            'field': 'contenu',
            'title': '内容',
            'sortable': True,
        },{
            'field': 'date_motifier',
            'title': '修改时间',
            'sortable': True,
        }, {
            'field': 'user_id',
            'title': '用户ID',
            'sortable': True,
        }, {
            'field': 'user_name',
            'title': '用户名',
            'sortable': True,
        }]
        value_list=['id']
        for column in columns:
            value_list.append(column['field'])
        columns1=table_header(columns,cathe)
        datas = models.pray.objects.order_by('-id').all().values(*value_list)
        list_data=json.dumps(list(datas),cls=DateEncoder)
        return render(request, "admin/liste.html", locals())

def app_index(request, fun, num):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/")
    else:
        user_info = request.session.get('user', None)
        if user_info['role'] > 11:
            return redirect("/")
    sidemenu = sidemenus
    cathe = 'app_index'
    titre = 'app首页'
    hide_lable = {'user_id': False,
                  'user_name': False,
                  'maison_name': False,
                  'maison': False
                  }
    les_class = {
        'user_id': [False, 'col', False],
        'user_name': [False, 'col', False],
        'maison_name': [False, 'col', False],
        'maison': [False, 'col', False],
    }
    tag_special = {
        'fichier_audio': 'button_audio',
        'fichier_video': 'button_video',
    }
    droit = ['observation']
    if (fun == "list"):
        columns = [{
            'field': 'title',
            'title': '主题',
            'sortable': True,
            'formatter': '''function (value, row, index) {
                return '<a href="/''' + cathe + '''/edit_form/'+row.id+'">'+value+'</a>'
                }'''
        },{
            'field': 'cathegory__titre',
            'title': '分类',
            'sortable': True,
            'formatter': 'fun_app_index_cathegory'
        },{
            'field': 'type',
            'title': '类型',
            'sortable': True,
            'formatter':'fun_app_index_type'
        },{
            'field': 'days',
            'title': '显示天数',
            'sortable': True,
            'formatter': 'fun_app_index_days'
        }, {
            'field': 'date_creer',
            'title': '修改日期',
            'sortable': True,
        }, {
            'field': 'user_id__prenom',
            'title': '修改人',
            'sortable': True,
        }]
        value_list = ['id',"parent__id"]
        for column in columns:
            value_list.append(column['field'])
        columns1 = table_header(columns, cathe)
        datas = models.app_index.objects.order_by('-id').filter(id__gt=1).values(*value_list)
        list_data = json.dumps(list(datas), cls=DateEncoder)
        return render(request, "admin/liste.html", locals())
    elif (fun == "new_form"):
        if request.method != 'POST':
            vaules = ''
            les_forms = models.app_index_input(user_info=user_info)
        else:
            les_forms = models.app_index_input(data=request.POST, user_info=user_info)
            if les_forms.is_valid():
                les_forms.save()
                return redirect('/' + cathe + '/list/0')
        return render(request, "admin/form2.html", locals())
    elif (fun == "edit_form"):
        vaules = models.app_index.objects.get(id=num)
        if request.method != 'POST':
            # 如果不是post,创建一个表单，并用instance=article当前数据填充表单
            les_forms = models.app_index_input(instance=vaules, user_info=user_info)
        else:
            les_forms = models.app_index_input(instance=vaules, data=request.POST, user_info=user_info)
            les_forms.save()  # 保存
            if les_forms.is_valid():  # 验证
                return redirect('/' + cathe + '/list/0')  # 成功跳转
        return render(request, "admin/form2.html", locals())
    elif fun == 'delete':
        vaules = models.app_index.objects.get(id=num)
        models.app_index.objects.get(id=num).delete()
        return redirect('/' + cathe + '/list/0')  # 成功跳转