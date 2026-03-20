from django.shortcuts import render,HttpResponse
from . import forms
from . import models
from . import commun
from django.shortcuts import redirect
# Create your views here.
import hashlib
import datetime
from django.conf import settings
import time
import os
import json
import re
from PIL import Image
from mutagen.mp3 import MP3
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.mail import EmailMessage
import random
import string
from django.db.models import Sum
from django.db.models import Q
import logging
from django.forms.models import model_to_dict
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from pydub import AudioSegment
import shutil
import sys
logger = logging.getLogger('django')

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj,datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self,obj)



def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def save_resized_image(uploaded_file_path, output_path, size=(300, 300)):
    print(uploaded_file_path)
    print(output_path)
    """
    将上传的图片调整为指定大小并保存。

    Args:
    - uploaded_file_path: str, 上传的图片路径。
    - output_path: str, 调整后图片保存路径。
    - size: tuple, 目标图片尺寸，默认是 (300, 300)。

    Returns:
    - None
    """
    # try:
        # 打开图片
    with Image.open(uploaded_file_path) as img:
        # 调整大小（会保持原图比例并填充背景）
        if img.mode == "RGBA":
            img = img.convert("RGB")

        # 保存图片
        target_width, target_height = size
        img_width, img_height = img.size

        # 计算缩放比例
        scale = max(target_width / img_width, target_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # 缩放图片
        img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

        # 计算裁剪区域
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height

        # 裁剪中间部分
        img_cropped = img_resized.crop((left, top, right, bottom))

        # 保存结果
        img_cropped.save(output_path, format="JPEG")
        print(f"图片已保存到 {output_path}")
    # except Exception as e:
    #     print(f"处理图片时出错: {e}")


@csrf_exempt
def helper(request,type):
    if not request.session.get('is_login', None):
        return HttpResponse("fail")
    else:
        user_info = request.session.get('user', None)
    # if(type=="uploadfile"):
    #     if request.method == "POST":
    #         # secret_id = ''  # 替换为用户的 secretId
    #         # secret_key = ''  # 替换为用户的 secretKey
    #         # region = 'ap-hongkong'  # 替换为用户的 Region
    #         # token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    #         # scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    #         # config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    #         # # 2. 获取客户端对象
    #         # client = CosS3Client(config)
    #         # print(client.__dict__)
    #         # response = client.list_buckets(
    #         # )
    #         # print(response)
    #         # print("POST-->", request.POST)
    #
    #         reqfile = request.FILES.get("file")
    #         an=time.strftime("%Y") + '/'
    #         path1='static/upload/' + an
    #         if not os.path.exists(path1):
    #             os.mkdir(path1)
    #         floder=an+time.strftime("%m")+'/'
    #         path = 'static/upload/' + floder
    #         if not os.path.exists(path):
    #             os.mkdir(path)
    #         now = time.strftime("%Y%m%d%H%M%S")
    #         file_type=os.path.splitext(path+now+'-'+reqfile.name)[-1][1:]
    #         file_type=file_type.lower()
    #         duration = 0
    #         stantard=''
    #         thumb=''
    #         file_name=reqfile.name.replace(' ', '_')
    #         if(file_type=="png" or file_type=="jpeg" or file_type=="jpg"):
    #             type='image'
    #             post=request.POST
    #             if('type' in post):
    #                 if(post['type']=='enseign'):
    #                     image = Image.open(reqfile)
    #                     image.save(path + now + "-" + file_name)
    #                     if (image.width / image.height > 1.5):
    #                         zoom = image.resize((image.width * 600 // image.height, 600))
    #                         box = ((zoom.width - 600) / 2, 0, (zoom.width - 600) / 2 + 600, 600)  ##确定拷贝区域大小
    #                         couper = zoom.crop(box)
    #                     else:
    #                         zoom = image.resize((600, image.height * 600 // image.width))
    #                         box = (0, (zoom.height - 600) / 2, 600, (zoom.height - 600) / 2 + 600)  ##确定拷贝区域大小
    #                         couper = zoom.crop(box)
    #                     couper.save(path + now + '-' + 'standard' + "-" + file_name)
    #                     couper.thumbnail((300, 300), Image.ANTIALIAS)
    #                     couper.save(path + now + '-' + 'thumbnail' + "-" + file_name)
    #                     stantard = now + '-' + 'standard' + "-" + file_name
    #                     thumb = now + '-' + 'thumbnail' + "-" + file_name
    #                     duration = 0
    #             else:
    #                 image = Image.open(reqfile)
    #                 image.save(path + now + "-" + file_name)
    #                 if(image.width/image.height>1.5):
    #                     zoom=image.resize((image.width*400//image.height, 400))
    #                     box = ((zoom.width-600)/2, 0, (zoom.width-600)/2+600, 400) ##确定拷贝区域大小
    #                     couper = zoom.crop(box)
    #                 else:
    #                     zoom=image.resize((600, image.height * 600 // image.width))
    #                     box = (0, (zoom.height - 400) / 2, 600 ,(zoom.height - 400) / 2 + 400)  ##确定拷贝区域大小
    #                     couper = zoom.crop(box)
    #                 couper.save(path + now + '-' + 'standard' + "-" + file_name)
    #                 couper.thumbnail((300, 200), Image.ANTIALIAS)
    #                 couper.save(path+now+'-'+'thumbnail'+"-"+file_name)
    #                 stantard = now + '-' + 'standard' + "-" + file_name
    #                 thumb = now + '-' + 'thumbnail' + "-" + file_name
    #                 duration=0
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + '-' + 'standard' + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + '-' + 'standard' + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + '-' + 'thumbnail' + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + '-' + 'thumbnail' + "-" +file_name,  # 上传到桶之后的文件名
    #             # )
    #         elif(file_type=="mp3" or file_type=="wma"):
    #             type = 'audio'
    #             with open(path + now + '-' + file_name, "wb") as f:
    #                 for line in reqfile:
    #                     f.write(line)
    #             audio = MP3(path + now + '-' + file_name)
    #             if audio.info.bitrate != 128000:
    #                 l_path=path + now + '-' + file_name
    #                 (src, name) = os.path.split(l_path)
    #                 new_path = "static/upload/old1/" + name
    #                 shutil.copy(l_path, new_path)
    #                 sound = AudioSegment.from_mp3(new_path)
    #                 file_handle = sound.export(l_path, format="mp3", bitrate="128k")
    #                 audio = MP3(l_path)
    #             duration=audio.info.length
    #             stantard = 'audio.jpg'
    #             thumb = 'audio.jpg'
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #         else:
    #             type=file_type
    #             duration=0
    #             thumb=file_type+'.jpg'
    #             stantard = file_type + '.jpg'
    #             with open(path + now + '-' + file_name, "wb") as f:
    #                 for line in reqfile:
    #                     f.write(line)
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #         obj = models.dossiers(
    #             nom_org = reqfile,
    #             nom= now + "-" + file_name,
    #             type=type,
    #             lien='/'+path,
    #             duration=duration,
    #             stantard=stantard,
    #             thumb=thumb,
    #             user_id=user_info['id'],
    #         )
    #         obj.save()
    #         if(obj.id):
    #             res="suc"
    #         else:
    #             res="fail"
    #     return HttpResponse(res)
    # if (type == "uploadfile"):
    #     if request.method == "POST":
    #         secret_id = ' # 替换为用户的 secretId
    #         secret_key =  # 替换为用户的 secretKey
    #         region = 'ap-hongkong'  # 替换为用户的 Region
    #         token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
    #         scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    #         config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    #         # 2. 获取客户端对象
    #         client = CosS3Client(config)
    #         # print(client.__dict__)
    #         response = client.list_buckets(
    #         )
    #         # print(response)
    #         # print("POST-->", request.POST)
    #
    #         reqfile = request.FILES.get("file")
    #         an = time.strftime("%Y") + '/'
    #         path1 = 'static/upload/' + an
    #         if not os.path.exists(path1):
    #             os.mkdir(path1)
    #         floder = an + time.strftime("%m") + '/'
    #         path = 'static/upload/' + floder
    #         if not os.path.exists(path):
    #             os.mkdir(path)
    #         now = time.strftime("%Y%m%d%H%M%S")
    #         file_type = os.path.splitext(path + now + '-' + reqfile.name)[-1][1:]
    #         file_type = file_type.lower()
    #         duration = 0
    #         stantard = ''
    #         thumb = ''
    #         file_name = reqfile.name.replace(' ', '_')
    #         url_path = '/'
    #         if (file_type == "png" or file_type == "jpeg" or file_type == "jpg" or file_type=="webp"):
    #             url_path += path
    #             type = 'image'
    #             post = request.POST
    #             if ('type' in post):
    #                 if (post['type'] == 'enseign'):
    #                     image = Image.open(reqfile)
    #                     image.save(path + now + "-" + file_name)
    #                     if (image.width / image.height > 1.5):
    #                         zoom = image.resize((image.width * 600 // image.height, 600))
    #                         box = ((zoom.width - 600) / 2, 0, (zoom.width - 600) / 2 + 600, 600)  ##确定拷贝区域大小
    #                         couper = zoom.crop(box)
    #                     else:
    #                         zoom = image.resize((600, image.height * 600 // image.width))
    #                         box = (0, (zoom.height - 600) / 2, 600, (zoom.height - 600) / 2 + 600)  ##确定拷贝区域大小
    #                         couper = zoom.crop(box)
    #                     couper.save(path + now + '-' + 'standard' + "-" + file_name)
    #                     couper.thumbnail((300, 300), Image.ANTIALIAS)
    #                     couper.save(path + now + '-' + 'thumbnail' + "-" + file_name)
    #                     stantard = now + '-' + 'standard' + "-" + file_name
    #                     thumb = now + '-' + 'thumbnail' + "-" + file_name
    #                     duration = 0
    #             else:
    #                 image = Image.open(reqfile)
    #                 image.save(path + now + "-" + file_name)
    #                 if (image.width / image.height > 1.5):
    #                     zoom = image.resize((image.width * 400 // image.height, 400))
    #                     box = ((zoom.width - 600) / 2, 0, (zoom.width - 600) / 2 + 600, 400)  ##确定拷贝区域大小
    #                     couper = zoom.crop(box)
    #                 else:
    #                     zoom = image.resize((600, image.height * 600 // image.width))
    #                     box = (0, (zoom.height - 400) / 2, 600, (zoom.height - 400) / 2 + 400)  ##确定拷贝区域大小
    #                     couper = zoom.crop(box)
    #                 couper.save(path + now + '-' + 'standard' + "-" + file_name)
    #                 couper.thumbnail((300, 200), Image.ANTIALIAS)
    #                 couper.save(path + now + '-' + 'thumbnail' + "-" + file_name)
    #                 stantard = now + '-' + 'standard' + "-" + file_name
    #                 thumb = now + '-' + 'thumbnail' + "-" + file_name
    #                 duration = 0
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + '-' + 'standard' + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + '-' + 'standard' + "-" + file_name,  # 上传到桶之后的文件名
    #             # )
    #             # response = client.upload_file(
    #             #     Bucket='yzzhenli-1256427631',
    #             #     LocalFilePath=path + now + '-' + 'thumbnail' + "-" + file_name,  # 本地文件的路径
    #             #     Key=floder + now + '-' + 'thumbnail' + "-" +file_name,  # 上传到桶之后的文件名
    #             # )
    #
    #             save_resized_image(path + now + "-" + file_name,path + now + '-' + 'icon' + "-" + file_name)
    #         elif (file_type == "mp3" or file_type == "wma"):
    #             type = 'audio'
    #             with open(path + now + '-' + file_name, "wb") as f:
    #                 for line in reqfile:
    #                     f.write(line)
    #             audio = MP3(path + now + '-' + file_name)
    #             # if audio.info.bitrate != 128000:
    #             #     l_path=path + now + '-' + file_name
    #             #     (src, name) = os.path.split(l_path)
    #             #     new_path = "static/upload/old1/" + name
    #             #     shutil.copy(l_path, new_path)
    #             #     sound = AudioSegment.from_mp3(new_path)
    #             #     file_handle = sound.export(l_path, format="mp3", bitrate="128k")
    #             #     audio = MP3(l_path)
    #             duration = audio.info.length
    #             stantard = 'audio.jpg'
    #             thumb = 'audio.jpg'
    #             print("正在上传")
    #             response = client.upload_file(
    #                 Bucket='yzzhenli-1256427631',
    #                 LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #                 Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             )
    #             print(response)
    #             url_path = "https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com/" + floder
    #             os.remove(path + now + '-' + file_name)
    #             print(url_path)
    #         else:
    #             type = file_type
    #             duration = 0
    #             thumb = file_type + '.jpg'
    #             stantard = file_type + '.jpg'
    #             with open(path + now + '-' + file_name, "wb") as f:
    #                 for line in reqfile:
    #                     f.write(line)
    #             response = client.upload_file(
    #                 Bucket='yzzhenli-1256427631',
    #                 LocalFilePath=path + now + "-" + file_name,  # 本地文件的路径
    #                 Key=floder + now + "-" + file_name,  # 上传到桶之后的文件名
    #             )
    #             url_path = "https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com/" + path
    #         obj = models.dossiers(
    #             nom_org=reqfile,
    #             nom=now + "-" + file_name,
    #             type=type,
    #             # lien='/'+path,
    #             lien=url_path,
    #             duration=duration,
    #             stantard=stantard,
    #             thumb=thumb,
    #             user_id=user_info['id'],
    #         )
    #         obj.save()
    #         if (obj.id):
    #             res = "suc"
    #         else:
    #             res = "fail"
    #     return HttpResponse(res)
    if (type == "uploadfile"):
        res=""
        b2=commun.B2()
        res=b2.upload_file_view(request)
        return HttpResponse(res)
    elif (type == "dossier"):
        data=request.POST
        n=int(data["n"])
        if "type" in data:
            if data["type"]:
                if data["type"]=="setting":
                    vaules = models.dossiers.objects.order_by('-id').filter()[20 * n:20 * (n + 1)].values()
                else:
                    vaules = models.dossiers.objects.order_by('-id').filter(type=data["type"])[20*n:20*(n+1)].values()
            else:
                vaules = models.dossiers.objects.order_by('-id').filter()[20 * n:20 * (n + 1)].values()
        else:
            vaules = models.dossiers.objects.order_by('-id').filter()[20 * n:20 * (n + 1)].values()
        vaules=list(vaules)
        return HttpResponse(json.dumps(vaules,cls=DateEncoder))
    elif (type == "ajouter_video"):
        data = request.POST
        obj = models.dossiers(
            nom_org=data['nom_org'],
            type=data['type'],
            lien=data['lien'],
            thumb='video.jpg',
            user_id=user_info['id'],
        )
        obj.save()
        if (obj.id):
            res = "suc"
        else:
            res = "fail"
        return HttpResponse(json.dumps(res))
    elif (type == "supprimer_dossier"):
        data = request.POST
        num=int(data["id"])
        detail=models.dossiers.objects.get(id=num)
        models.dossiers.objects.get(id=num).delete()
        path = detail.lien+detail.nom  # 文件路径
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)
        path = detail.lien + detail.stantard  # 文件路径
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)
        path = detail.lien + detail.thumb  # 文件路径
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)
        return HttpResponse(json.dumps("suc"))
    elif type == "motie":
        res = models.article.objects.filter(~Q(fichier_audio=""),Q(id=8650)).values('id','fichier_audio')
        res=list(res)
        return HttpResponse(json.dumps(res))
    elif type == "motie_js":
        data = request.POST
        logger.warning(data)
        src = data['fichier_audio']
        src = src.replace("https://yzzhenli-1256427631.cos.ap-hongkong.myqcloud.com", "static/upload");
        src = src.replace("/static/", "static/")
        duration=0
        logger.warning(src)
        if os.path.exists(src):
            audio = MP3(src)
            duration = audio.info.length
            models.article.objects.filter(id=data['id']).update(duration=int(duration))
        return HttpResponse(json.dumps(duration))



def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

@csrf_exempt
def helper_cur(request, type):
    if type == 'activite_login':
        data = request.POST
        email=data['email']
        password = data['password']
        try:
            user = models.compte.objects.get(email=email)
        except:
            message = 'exsit pas'
            return HttpResponse(json.dumps(message))
        if user.mots_passe == hash_code(password):
            request.session['is_login'] = True
            request.session['user'] = {'id': user.id, 'role': user.role, 'maison': user.id, 'nom': user.prenom,
                                       'nom_maison': user.nom_maison, 'visuel': user.visuel, 'question': 0}
            values = models.compte.objects.filter(email=email).values('id','prenom','nom','naissance','adresse','code_postal','Tel','etat_vie')  # 修改
            values = list(values)
            return HttpResponse(json.dumps(values[0], cls=DateEncoder))
        else:
            message = 'corresponds pas'
            return HttpResponse(json.dumps(message))
        # return HttpResponse(json.dumps(password))
    elif type=="get_articles":
        data = request.POST
        articles=models.article.objects.order_by('-date_publier').filter(cathegorie=data['num'])[(int(data["page"])-1)*int(data["per_page"]):int(data["page"])*int(data["per_page"])].values("id","title","date_publier","visuel")
        res=list(articles)
        return HttpResponse(json.dumps(res,cls=DateEncoder))
    elif type == "get_courses":

        data = request.POST
        articles = models.cours.objects.order_by('-id').filter(parent=0)[
                   (int(data["page"]) - 1) * int(data["per_page"]):int(data["page"]) * int(data["per_page"])].values(
            "id", "title","visuel")
        res = list(articles)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
@xframe_options_exempt
def tinymc(request,fun):
    if not request.session.get('is_login', None):
        return HttpResponse("fail")
    else:
        user_info = request.session.get('user', None)
    if fun=="admin_TinyMCE":
        return render(request, "admin/tinymce.html", locals())
    if fun=="iframe":
        data=request.GET
        if(data['type']=="audio"):
            audio=True
        else:
            audio=False
        if (data['type'] == "video"):
            video = True
        else:
            video = False
        return render(request, "admin/tinymce_frame.html", locals())
    if fun=="emailtag":
        inputs = models.inscriptions_vip_input_setting(contenu={})
        ext=['formule','venue_imminente_reponse','venue_imminente','confirmer_reponse','email_confirmer']
        # for un in ext:
        #     inputs.pop[un]
        return render(request, "admin/tinymce_emailtag.html", locals())
    if fun=="printtag":
        get = request.GET
        data = models.prints.objects.get(id=get['id'])
        if(data.data=='inscription_pro'):
            titre="Hébergement"
            inputs = models.inscriptions_vip_input_setting(contenu={})
        if (data.data == 'facture'):
            #imprimer/parametres 起作用
            res = {'activite': {'name': 'activite', 'label': 'Activité'},
                   'description': {'name': 'description', 'label': 'Description'},
                   'prix': {'name': 'prix', 'label': 'Prix'},
                   'nom': {'name': 'nom', 'label': 'Nom'},
                   'prenom': {'name': 'prenom', 'label': 'Prénom'},
                   'email': {'name': 'email', 'label': 'Email'},
                   }
            if user_info['role'] == 0:
                res['taxe'] = {'name': 'taxe', 'label': 'Taxe'}
            res = json.dumps(res)
        return render(request, "admin/tinymce_printtag.html", locals())


def envoyer_un_email(maison_id,adresse,subjet,contenu):
    maison = models.compte.objects.get(id=maison_id)
    print(maison.nom_maison)
    email = EmailMessage(
        subjet,
        contenu,
        maison.nom_maison +' Par',
        [adresse],
        reply_to=[maison.email],
        # headers={'Message-ID': 'foo'},
    )
    email.content_subtype = "html"
    r = email.send()
    return r

@csrf_exempt
def listdata(request,type):
    if not request.session.get('is_login', None):
        return HttpResponse("fail")
    else:
        user_info = request.session.get('user', None)
    if (type == "contact"):
        vaules = models.contact.objects.order_by('-id').filter(maison=user_info['maison']).values()
        vaules = list(vaules)
        return HttpResponse(json.dumps(vaules, cls=DateEncoder))
    elif (type == "facture"):
        if user_info['role']==0:
            datas = models.paiement.objects.order_by('-id').all()
        else:
            datas = models.paiement.objects.order_by('-id').filter(maison=user_info['maison'])
        new_data=[]
        for un in datas:
            if models.inscriptions.objects.filter(id=un.inscription).exists():
                new_data.append({
                    'id':un.id,
                    'prix':un.prix,
                    'description':un.description,
                    'type':un.type,
                    'date_creer':un.date_creer,
                    'activite':un.activite,
                    'Statue':un.Statue,
                    'nom':un.inscri_detail.nom,
                    'prenom': un.inscri_detail.prenom,
                    'email':un.inscri_detail.email,
                    'adresse': un.inscri_detail.adresse,
                    'code_postal': un.inscri_detail.code_postal,
                    'ville': un.inscri_detail.ville,
                    'pays': un.inscri_detail.pays,
                    'taxe': un.taxe,
                    'recevoir': un.recevoir,
                    'numero_fa_frais': un.numero_fa_frais,
                    'numero_facture': un.numero_facture,
                    'maison':un.maison,
                    'maison_name':un.maison_name,
                    'retour': un.retour,
                })
            else:
                user=models.compte.objects.get(id=un.user_id)
                new_data.append({
                    'id': un.id,
                    'prix': un.prix,
                    'description': un.description,
                    'type': un.type,
                    'date_creer': un.date_creer,
                    'activite': un.activite,
                    'Statue': un.Statue,
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'email': user.email,
                    'adresse': user.adresse,
                    'code_postal': user.code_postal,
                    'ville': user.ville,
                    'pays': user.pays,
                    'taxe': un.taxe,
                    'recevoir': un.recevoir,
                    'numero_fa_frais': un.numero_fa_frais,
                    'numero_facture': un.numero_facture,
                    'maison': un.maison,
                    'maison_name': un.maison_name,
                    'retour': un.retour,
                })
        return HttpResponse(json.dumps(new_data, cls=DateEncoder))
    elif (type == "event_home"):
        datas = models.event_maison.objects.order_by('-id').filter(maison=user_info['maison']).values()
        vaules = list(datas)
        return HttpResponse(json.dumps(vaules, cls=DateEncoder))


def help(request, type):
    if type=='ecouter':
        data = request.POST
        if data['b_type']=='quotidiens':
            res=models.quotidien.objects.get(id=data['num'])
            res={'audio':res.fichier_audio,'video':res.fichier_video,'title':res.title,'contenu':res.contenu,'auteur':res.auteur}
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif type=='prier':
        data = request.POST
        res=models.prieres.objects.filter(id=data['num']).update(bon=int(data['nombre'])+1)
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif (type == "dasaigequ"):
        data=request.POST
        news_cathe = models.cathegorie.objects.filter(parent=26)
        new_news_cathe = [26]
        for un in news_cathe:
            new_news_cathe.append(un.id)
        print(data)
        if int(data['id'])==0:
            articles = models.article.objects.order_by('-id').filter(Q(cathegorie__in=new_news_cathe),~Q(fichier_audio=''))[:1]
        else:
            if data['fun']=='next':
                articles = models.article.objects.order_by('-id').filter(Q(cathegorie__in=new_news_cathe),
                                                                         ~Q(fichier_audio__isnull=True), Q(id__lt=data['id']))[:1]
            else:
                articles = models.article.objects.order_by('-id').filter(Q(cathegorie__in=new_news_cathe),
                                                                         ~Q(fichier_audio__isnull=True), Q(id__gt=data['id']))[:1]
        if len(articles)>0:
            res={'id':articles[0].id,'audio':articles[0].fichier_audio}
        else:
            res=0

        print(res)
        return HttpResponse(json.dumps(res,cls=DateEncoder))
    elif type == "delete_prayer":
        try:
            data = request.POST
            models.pray.objects.filter(id=data['id']).delete()
            res="ok"
        except:
            res="fail"
        return HttpResponse(json.dumps(res, cls=DateEncoder))
    elif type == "forbid_prayer":
        data = request.POST
        print(data)
        prayer=models.pray.objects.get(id=data['id'])
        print(prayer.user_id)
        models.compte.objects.filter(id=prayer.user_id).update(role=25)
        res="ok"
        return HttpResponse(json.dumps(res, cls=DateEncoder))