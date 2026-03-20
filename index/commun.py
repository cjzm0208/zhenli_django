import datetime
import time
from . import models
import random
import re
from django.conf import settings
# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client
from tencentcloud.sms.v20210111 import models as models_sms
# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils.encoding import force_str
import b2sdk.v2 as b2
from PIL import Image
from mutagen.mp3 import MP3
import uuid
import os
import shutil
import subprocess
import json
import logging
from pydub import AudioSegment
import requests
logger = logging.getLogger('django')
class keyword():
    def __init__(self,request):
        self.request = request
    def find(self,num):
        try:
            # 必要步骤：
            # 实例化一个认证对象，入参需要传入腾讯云账户密钥对secretId，secretKey。
            # 这里采用的是从环境变量读取的方式，需要在环境变量中先设置这两个值。
            # 你也可以直接在代码中写死密钥对，但是小心不要将代码复制、上传或者分享给他人，
            # 以免泄露密钥对危及你的财产安全。
            # CAM密匙查询: https://console.cloud.tencent.com/cam/capi
            cred = credential.Credential(os.getenv("TENCENT_SECRET_ID"), os.getenv("TENCENT_SECRET_KEY"))
            # cred = credential.Credential(
            #     os.environ.get(""),
            #     os.environ.get("")
            # )

            # 实例化一个http选项，可选的，没有特殊需求可以跳过。
            httpProfile = HttpProfile()
            # 如果需要指定proxy访问接口，可以按照如下方式初始化hp
            # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
            httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
            httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
            httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

            # 非必要步骤:
            # 实例化一个客户端配置对象，可以指定超时时间等配置
            clientProfile = ClientProfile()
            # HmacSHA256
            clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
            clientProfile.language = "en-US"
            clientProfile.httpProfile = httpProfile

            # 实例化要请求产品(以sms为例)的client对象
            # 第二个参数是地域信息，可以直接填写字符串ap-guangzhou，或者引用预设的常量
            client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

            # 实例化一个请求对象，根据调用的接口和实际情况，可以进一步设置请求参数
            # 你可以直接查询SDK源码确定SendSmsRequest有哪些属性可以设置
            # 属性可能是基本类型，也可能引用了另一个数据结构
            # 推荐使用IDE进行开发，可以方便的跳转查阅各个接口和数据结构的文档说明
            req = models_sms.SendSmsRequest()

            # 基本类型的设置:
            # SDK采用的是指针风格指定参数，即使对于基本类型你也需要用指针来对参数赋值。
            # SDK提供对基本类型的指针引用封装函数
            # 帮助链接：
            # 短信控制台: https://console.cloud.tencent.com/smsv2
            # sms helper: https://cloud.tencent.com/document/product/382/3773

            # 短信应用ID: 短信SdkAppId在 [短信控制台] 添加应用后生成的实际SdkAppId，示例如1400006666
            req.SmsSdkAppId = "1400579008"
            # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，签名信息可登录 [短信控制台] 查看
            req.SignName = "河北仆人文化传媒有限公司"
            # 短信码号扩展号: 默认未开通，如需开通请联系 [sms helper]
            req.ExtendCode = ""
            # 用户的 session 内容: 可以携带用户侧 ID 等上下文信息，server 会原样返回
            req.SessionContext = "xxx"
            # 国际/港澳台短信 senderid: 国内短信填空，默认未开通，如需开通请联系 [sms helper]
            req.SenderId = ""
            # 下发手机号码，采用 E.164 标准，+[国家或地区码][手机号]
            # 示例如：+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
            req.PhoneNumberSet = ["+86"+str(num)]
            # 模板 ID: 必须填写已审核通过的模板 ID。模板ID可登录 [短信控制台] 查看
            req.TemplateId = "1148403"
            # 模板参数: 若无模板参数，则设置为空
            rad=random.randint(10000, 99999)
            req.TemplateParamSet = [str(rad),'30']

            # 通过client对象调用DescribeInstances方法发起请求。注意请求方法名与请求对象是对应的。
            # 返回的resp是一个DescribeInstancesResponse类的实例，与请求对象对应。
            resp = client.SendSms(req)
            models.verifi_code.objects.create(tel=num,code=rad,date_creer=datetime.datetime.now())
            # 输出json格式的字符串回包
            return 1
            # print(resp.to_json_string(indent=2))
        except TencentCloudSDKException as err:
            print(err)
            return 0

class Setting():
    def __init__(self,request):
        self.request = request
    def setting_general(self):
        index_image_logo = models.setting.objects.get(key="index_image_logo")
        index_image_logo_lien = models.setting.objects.get(key="index_image_logo_lien")
        return {'index_image_logo_lien':index_image_logo_lien.contenu,'index_image_logo':index_image_logo.contenu}
    def setting_index(self):
        values_setting = models.setting.objects.all()
        values_settings = {}
        for un in values_setting:
            values_settings[un.key] = un.contenu
        return values_settings

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super(LazyEncoder, self).default(obj)


def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return bool(pattern.search(text))
def keep_chinese(text):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    return re.sub(pattern, '', text)
def remove_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    return re.sub(pattern, '', text)

class Office():
    def lecture(self,date_str):
        print(date_str)
        l_date = time.strptime(date_str, '%Y-%m-%d')
        annee = l_date.tm_year
        month = l_date.tm_mon
        jour = l_date.tm_mday
        ce_jour = datetime.date(annee, month, jour)
        abc = (annee - 2008) % 3
        impaire = (annee) % 2
        N = annee - 1900
        A = N % 19
        Q = N // 4
        B = (7 * A + 1) // 19
        M = (11 * A + 4 - B) % 29
        W = (N + Q + 31 - M) % 7
        D = 25 - M - W
        if (D > 0):
            jour = D
            mois = 4
        elif (D < 0):
            jour = D + 31
            mois = 3
        else:
            jour = 31
            mois = 3
        le_paque = datetime.date(annee, mois, jour)
        date_special = {'paque': le_paque}
        date_special['cendres'] = le_paque - datetime.timedelta(days=46)
        date_special['pentecote'] = le_paque + datetime.timedelta(days=49)
        date_special['la_triniter'] = date_special['pentecote'] + datetime.timedelta(days=7)
        date_special['le_saint_sacrement'] = date_special['la_triniter'] + datetime.timedelta(days=4)
        date_special['le_saint_coeur'] = date_special['le_saint_sacrement'] + datetime.timedelta(days=4)
        date_special['noel'] = datetime.date(annee, 12, 25)
        date_special['N1_0'] = date_special['noel'] - datetime.timedelta(days=7 - 1 - date_special['noel'].weekday())
        date_special['A1_0'] = date_special['noel'] - datetime.timedelta(days=21 + 1 + date_special['noel'].weekday())
        date_special['christ_roi'] = date_special['A1_0'] - datetime.timedelta(days=7)
        le_nouvel_an = datetime.date(annee, 1, 1)
        jour_nouvel_an = le_nouvel_an.weekday()
        i = jour_nouvel_an
        day = le_nouvel_an
        s_premier_O=0
        if jour_nouvel_an == 0 or jour_nouvel_an == 6:
            while i < 15:
                day = day + datetime.timedelta(days=1)
                i += 1
                if (i == 6):
                    date_special['epiphanie'] = day
                elif (i == 7):
                    date_special['bapteme'] = day  # bapteme
                    s_premier_O = (date_special['cendres'] - date_special['bapteme']).days // 7 + 1
                elif i < 7:
                    date_special['E_avant_' + str(day.weekday() + 1)] = day
        else:
            while i < 15:
                day = day + datetime.timedelta(days=1)
                i += 1
                if (i == 6):
                    date_special['epiphanie'] = day
                elif (i == 13):
                    date_special['bapteme'] = day  # bapteme
                    s_premier_O = (date_special['cendres'] - date_special['bapteme']).days // 7 + 1
                elif i < 6:
                    date_special['E_avant_' + str(day.weekday() + 1)] = day
                elif i > 6 and i < 13:
                    date_special['E_apres_' + str(day.weekday() + 1)] = day
        que_jour = ce_jour.strftime("%m_%d")
        fete = ''
        for k, v in date_special.items():
            if ce_jour == v:
                fete = k
        if models.sg_lecture.objects.filter(sign=que_jour).exists():
            f = que_jour
        else:
            j = (ce_jour.weekday() + 1) % 7
            if ce_jour > date_special['bapteme'] and ce_jour < date_special['cendres']:
                s = (ce_jour - date_special['bapteme']).days // 7 + 1
                f = "O" + str(s) + '_' + str(j)
            elif ce_jour > date_special['cendres'] and ce_jour < date_special['paque']:
                s = ((ce_jour - date_special['cendres']).days + 3) // 7 + 1
                f = "C" + str(s - 1) + '_' + str(j)
            elif ce_jour > date_special['paque'] and ce_jour < date_special['pentecote']:
                s = (ce_jour - date_special['paque']).days // 7 + 1
                f = "P" + str(s) + '_' + str(j)
            elif ce_jour > date_special['pentecote'] and ce_jour < date_special['A1_0']:
                if date_special["pentecote"].weekday() !=6:
                    s = (ce_jour - date_special['pentecote']).days // 7 + 1 + s_premier_O + 1
                    f = "O" + str(s) + '_' + str(j)
                else:
                    s = (ce_jour - date_special['pentecote']).days // 7 + 1 + s_premier_O
                    f = "O" + str(s) + '_' + str(j)
            elif ce_jour > date_special['A1_0'] and ce_jour < date_special['noel']:
                abc = (abc + 1) % 3
                s = (ce_jour - date_special['A1_0']).days // 7 + 1
                f = "A" + str(s) + '_' + str(j)
            else:
                f = "error"
        mark=""
        print(date_special)
        res = []
        if fete:
            mark=fete
        else:
            mark = f
        return {"mark":mark,"impaire":impaire,"abc":abc}
    def chercher_messe(self,mark,impaire,abc):
        res = []
        lecture = models.sg_lecture.objects.filter(sign=mark).values()
        if len(lecture) == 1:
            res = lecture[0]
        elif len(lecture) == 2:
            for lec in lecture:
                if lec['impair'] == impaire:
                    res = lec
                    break
        elif len(lecture) == 3:
            for lec in lecture:
                if lec['abc'] == abc:
                    res = lec
                    break
        return res
    def chercher_bible(self,str):
        str=str.replace("：",":")
        str = str.replace("，", ",")
        str = str.replace("；", ";")
        new_str=[]
        current_book = ""
        for part in str.split(";"):
            if has_chinese(part):
                current_book=keep_chinese(part)
                models.sg_bibleBook.objects.get(brev=current_book)
                new_str.append([current_book,remove_chinese(part)])
            else:
                new_str.append([current_book, remove_chinese(part)])
        new_chapitre=[]
        current_chapitre = ""
        for chapitre in new_str:
            if ":" in chapitre[1]:
                chapitre_arr=chapitre[1].split(":")
                current_chapitre=chapitre_arr[0]
                new_chapitre.append([chapitre[0],current_chapitre,chapitre_arr[1]])
            else:
                new_chapitre.append([chapitre[0], current_chapitre, chapitre[1]])
        print(new_chapitre)
        new_verse=[]
        for verse in new_chapitre:
            for un_verse in verse[2].split(","):
                if "-" in un_verse:
                    verse_arr = un_verse.split("-")
                    result = list(range(int(verse_arr[0]), int(verse_arr[1]) + 1))
                    for un in result:
                        new_verse.append([verse[0],verse[1],un])
                else:
                    new_verse.append([verse[0], verse[1],un_verse])
        return new_verse
    def compare_bible(self,verse_list):
        List_verse_map = []
        for un in verse_list:
            bibleBook = models.sg_bibleBook.objects.get(brev=un[0])
            un.append(bibleBook.mark)
            verse = models.sg_bible.objects.get(livre=bibleBook.mark, chapitre=un[1], partie=un[2])
            List_verse_map.append({"livre": bibleBook.mark, "chapitre": un[1], "verse": un[2], "commun": verse.commun})
        return List_verse_map
    # def chercher_lecture(slef,url):
    #     try:
    #         page = urllib.request.urlopen(url)
    #         soup = BeautifulSoup(page, 'html.parser', from_encoding='CP950')
    #         contenu = soup.select('p')
    #         new_contenu=""
    #         for un in contenu:
    #             new_contenu+="<p>"+un.get_text()+"</p>"
    #         # if un_office == "messe":
    #         #     title = soup.select('.m-b-0')
    #         #     # title = re.sub('\\<.*?\\>', ' ', str(title[0]))
    #         #     messe1 = soup.select('#messe1')
    #         #     messe2 = soup.select('#messe2')
    #         #     messe3 = soup.select('#messe3')
    #         #     messe4 = soup.select('#messe4')
    #         #     res = messe1 + messe2 + messe3 + messe4
    #         #     return str(title[0]) + str(res[0])
    #         # else:
    #         #     res = soup.select('.block-single-reading')
    #         return new_contenu
    #     except:
    #         return False

    # def chercher_offices(self,mark,type):
    #     office=models.offices.objects.get(mark=mark)
    #     office=model_to_dict(office)
    #     return office[type]
    # def chercher_complies(self,mark):
    #     office=models.complies.objects.get(mark=mark)
    #     office=model_to_dict(office)
    #     return office["complie"]


class B2():
    def __init__(self):
        self.B2_INFO = {
            "key_id": os.getenv("B2_KEY_ID"),  # 你的 keyID
            "application_key": os.getenv("B2_APP_KEY"),  # 你的 applicationKey
            "bucket_name": "yzzhenli",  # 改成你自己的 bucket 名
            "public_url": "https://cdn.yzzhenli.com"  # 你用 Cloudflare 绑好的域名（或 f000.backblazeb2.com）
        }
        self.b2_api = b2.InMemoryAccountInfo()
        self.bucket = None


    def get_b2_bucket(self):
        if self.bucket is None:
            info = b2.InMemoryAccountInfo()
            b2_api = b2.B2Api(info)
            b2_api.authorize_account("production", self.B2_INFO["key_id"], self.B2_INFO["application_key"])
            self.bucket = b2_api.get_bucket_by_name(self.B2_INFO["bucket_name"])
        return self.bucket

    # def save_resized_image(self,src_path, dst_path, size=(600, 600)):
    #     """统一生成缩略图函数（你原来已经有）"""
    #     with Image.open(src_path) as img:
    #         img.thumbnail(size, Image.Resampling.LANCZOS)
    #         img.save(dst_path)

    def save_resized_image(self,uploaded_file_path, output_path, size=(300, 300)):
        # print(uploaded_file_path)
        # print(output_path)
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
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)

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

    def upload_to_b2(self,local_path: str, key_in_bucket: str):
        print(key_in_bucket)
        # print(local_path, key_in_bucket)
        # 关键两行：把 Windows 的 \ 全部换成 /
        key_in_bucket = key_in_bucket.replace("\\", "/")
        """上传单个文件并返回公开 URL"""
        bucket = B2.get_b2_bucket(self)
        with open(local_path, "rb") as f:
            res=bucket.upload_bytes(
            data_bytes=f.read(),
            file_name=key_in_bucket,
        )
            print(res)
        # 返回走 Cloudflare CDN 的公开链接
        return f"{self.B2_INFO['public_url']}/{key_in_bucket}"

    def upload_file_view(self,request):
        if request.method != "POST":
            return "fail"

        reqfile = request.FILES.get("file")
        if not reqfile:
            return "fail"

        # 生成路径：2025/12/20251208123456-xxx.mp4
        year = time.strftime("%Y")
        month = time.strftime("%m")
        prefix = f"{year}/{month}/"
        timestamp = time.strftime("%Y%m%d%H%M%S")
        uuid_str = uuid.uuid4().hex[:8]
        unique_name = f"{timestamp}-{uuid_str}-{reqfile.name.replace(' ', '_')}"
        file_type = os.path.splitext(reqfile.name)[1][1:].lower()

        # 临时保存到本地（Django 默认在 /tmp）
        upload_tmp_dir = os.path.join(settings.BASE_DIR, 'static', 'upload', 'tmp')
        os.makedirs(upload_tmp_dir, exist_ok=True)  # 确保主目录存在

        tmp_dir = os.path.join(upload_tmp_dir, prefix)  # 例如：2025/12/
        os.makedirs(tmp_dir, exist_ok=True)

        # unique_name = f"{timestamp}-{uuid_str}{os.path.splitext(reqfile.name)[1]}"
        # 4. 正确拼接路径（关键！只用 os.path.join）
        tmp_path = os.path.join(tmp_dir, unique_name)
        orignal = os.path.join(prefix, unique_name)

        # 保存上传的文件
        with open(tmp_path, "wb+") as destination:
            for chunk in reqfile.chunks():
                destination.write(chunk)
            print("存储结束")

        type_ = "other"
        duration = 0
        standard = ""
        thumb = ""
        url_path = ""
        standard_key=""
        thumb_key=""

        try:
            # ───── 图片处理 ─────
            if file_type in {"png", "jpg", "jpeg", "webp", "gif", "bmp"}:
                type_ = "image"
                standard = f"{prefix}{timestamp}-standard-{uuid_str}-{os.path.splitext(reqfile.name)[1]}"
                standard_key = os.path.join(tmp_dir, f"{timestamp}-standard-{uuid_str}-{reqfile.name.replace(' ', '_')}")
                thumb = f"{prefix}{timestamp}-thumbnail-{uuid_str}-{os.path.splitext(reqfile.name)[1]}"
                thumb_key = os.path.join(tmp_dir, f"{timestamp}-thumbnail-{uuid_str}-{reqfile.name.replace(' ', '_')}")
                # print(original_key)

                # 原图
                # B2.upload_to_b2(self,tmp_path, orignal)

                # 生成 standard（600px 高或宽）
                # std_path = tmp_path.replace(unique_name, f"standard-{unique_name}")
                B2.save_resized_image(self, tmp_path, standard_key, size=(600, 400))
                # B2.upload_to_b2(self,standard_key, standard)
                # 缩略图 300×300
                # thumb_path = tmp_path.replace(unique_name, f"thumb-{unique_name}")
                B2.save_resized_image(self,tmp_path, thumb_key, size=(300, 200))
                # B2.upload_to_b2(self,thumb_key, thumb)
                upload_dir = os.path.join(settings.BASE_DIR, 'static', 'upload', prefix)

                print(upload_dir)
                # 确保目标目录存在
                os.makedirs(upload_dir, exist_ok=True)
                destination_path_orignal = os.path.join(
                    upload_dir,
                    f"{timestamp}-{uuid_str}-{reqfile.name.replace(' ', '_')}"
                )
                print(destination_path_orignal)
                shutil.copy2(tmp_path, destination_path_orignal)
                # 目标文件的完整路径（和 standard 的文件名完全一致）
                destination_path_standard = os.path.join(
                    upload_dir,
                    f"{timestamp}-standard-{uuid_str}-{reqfile.name.replace(' ', '_')}"
                )

                # 方法1：推荐使用 shutil.copy2（保留元数据）
                shutil.copy2(standard_key, destination_path_standard)

                destination_path_thumbnail = os.path.join(
                    upload_dir,
                    f"{timestamp}-thumbnail-{uuid_str}-{reqfile.name.replace(' ', '_')}"
                )
                # 方法1：推荐使用 shutil.copy2（保留元数据）
                shutil.copy2(thumb_key, destination_path_thumbnail)


                # standard = standard_key
                # thumb = thumb_key

                # url_path = f"{self.B2_INFO['public_url']}/{prefix}"
                # standard = f"{timestamp}-standard-{uuid_str}{os.path.splitext(reqfile.name)[1]}"
                # thumb = f"{timestamp}-thumbnail-{uuid_str}{os.path.splitext(reqfile.name)[1]}"
                url_path = f"/static/upload/{prefix}"
                standard = f"{timestamp}-standard-{uuid_str}-{reqfile.name.replace(' ', '_')}"
                thumb = f"{timestamp}-standard-{uuid_str}-{reqfile.name.replace(' ', '_')}"
            # ───── 音频处理 ─────
            elif file_type in {"mp3", "wma", "wav", "flac", "m4a"}:
                type_ = "audio"
                key = prefix + unique_name
                tmp_path=B2.force_convert_to_mp3(self,tmp_path)
                B2.upload_to_b2(self,tmp_path, key)

                # 获取时长
                audio = MP3(tmp_path)
                duration = int(audio.info.length)

                standard = "audio.jpg"  # 你可以自己准备一张默认封面
                thumb = "audio.jpg"
                url_path = f"{self.B2_INFO['public_url']}/{prefix}"

            # ───── 视频/其他文件 ─────
            elif file_type in {"mp4", "mov", "avi", "mkv", "webm"}:
                type_ = "video"
                # base_name=f"{timestamp}-{uuid_str}"
                # video_output_dir = os.path.join(tmp_dir,base_name)
                # os.makedirs(video_output_dir, exist_ok=True)
                # transcoded_files=self.transcode_video(tmp_path, video_output_dir, base_name)
                # if not transcoded_files:
                #     print(f"    ✗ 转码失败")
                #     return False
                #
                # # 生成 HLS
                # hls_dir, hls_files = self.generate_hls(tmp_path, video_output_dir, base_name)
                #
                # # 上传所有文件
                # print(f"    上传到 B2...")
                # file_metadata = {
                #     'original_name': reqfile.name,
                #     # 'file_id': file_id,
                #     'upload_time': datetime.datetime.now().isoformat()
                # }
                #
                # upload_count = 0
                # B2_FOLDER=prefix
                #
                # # 上传转码后的 MP4 文件
                # for tf in transcoded_files:
                #     b2_path = f"{B2_FOLDER}{base_name}/{os.path.basename(tf['path'])}"
                #     print(tf)
                #     print(b2_path)
                #     if self.upload_to_b2_video(tf['path'], b2_path, file_metadata):
                #         upload_count += 1
                #
                # # 上传 HLS 文件
                # if hls_dir and hls_files:
                #     for hls_file in hls_files:
                #         print(hls_file)
                #         local_hls_path = os.path.join(hls_dir, hls_file)
                #         b2_hls_path = f"{B2_FOLDER}{base_name}/hls/{hls_file}"
                #         print(b2_hls_path)
                #         if self.upload_to_b2_video(local_hls_path, b2_hls_path, file_metadata):
                #             upload_count += 1
                #
                # print(f"      ✓ 已上传 {upload_count} 个文件")
                key = prefix + unique_name
                url_path=B2.upload_to_b2(self, tmp_path, key)
                standard = "video.jpg"  # 你可以自己准备一张默认封面
                thumb = "video.jpg"
                # url_path = f"{self.B2_INFO['public_url']}/{prefix}{base_name}/hls/playlist.m3u8"
                # url_path = f"{self.B2_INFO['public_url']}/{prefix}"

                # # 清理临时文件
                # if os.path.exists(tmp_path):
                #     os.remove(tmp_path)
                #
                # if os.path.exists(video_output_dir):
                #     shutil.rmtree(video_output_dir)

            else:
                type_ =  "file"
                key = prefix + unique_name
                B2.upload_to_b2(self,tmp_path, key)
                # 视频想取时长可以打开下面两行（需要 ffmpeg）
                # probe = ffmpeg.probe(tmp_path)
                # duration = int(float(probe['format']['duration']))
                standard = file_type + ".jpg"
                thumb = file_type + ".jpg"
                url_path = f"{self.B2_INFO['public_url']}/{prefix}"

            # ───── 入库 ─────
            obj = models.dossiers(
                nom_org=reqfile,
                nom=unique_name,
                type=type_,
                lien=url_path,  # 直接是 https://media.yourchurch.org/2025/12/xxx.mp4
                duration=duration,
                stantard=standard,
                thumb=thumb,
                user_id=request.user.id,  # 按你原来的逻辑
            )
            obj.save()
            result = "suc" if obj.id else "fail"
        finally:
            # 清理临时文件
            for p in [tmp_path, standard_key, thumb_key]:
                if p and os.path.exists(p):
                    os.remove(p)
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return "result"

    def get_video_info(self, video_path):
        """获取视频信息"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            print(f"    警告: 无法获取视频信息: {e}")
            return None
    def transcode_video(self, input_path, output_dir, base_name):
        """转码视频为多个分辨率"""
        print(f"    转码中...")
        RESOLUTIONS = {
            "1080p": {"width": 1920, "height": 1080, "bitrate": "5000k", "audio_bitrate": "192k"},
            "720p": {"width": 1280, "height": 720, "bitrate": "3000k", "audio_bitrate": "128k"},
            "480p": {"width": 854, "height": 480, "bitrate": "1500k", "audio_bitrate": "128k"},
            "360p": {"width": 640, "height": 360, "bitrate": "800k", "audio_bitrate": "96k"},
        }

        # 获取原始视频信息
        video_info = self.get_video_info(input_path)
        original_height = 1080  # 默认值

        if video_info:
            for stream in video_info.get('streams', []):
                if stream.get('codec_type') == 'video':
                    original_height = stream.get('height', 1080)
                    break

        transcoded_files = []

        # 为每个分辨率转码
        for res_name, res_config in RESOLUTIONS.items():
            # 如果原始分辨率小于目标分辨率,跳过
            if original_height < res_config['height']:
                print(f"      跳过 {res_name} (原始分辨率较低)")
                continue

            output_file = os.path.join(output_dir, f"{base_name}_{res_name}.mp4")

            # cmd = [
            #     'ffmpeg',
            #     '-i', input_path,
            #     '-c:v', 'libx264',  # 视频编码器
            #     '-preset', 'medium',  # 编码速度 (faster/fast/medium/slow)
            #     '-crf', '23',  # 质量控制 (18-28, 越小质量越好)
            #     '-vf', f"scale={res_config['width']}:{res_config['height']}",
            #     '-b:v', res_config['bitrate'],
            #     '-maxrate', res_config['bitrate'],
            #     '-bufsize', str(int(res_config['bitrate'].rstrip('k')) * 2) + 'k',
            #     '-c:a', 'aac',  # 音频编码器
            #     '-b:a', res_config['audio_bitrate'],
            #     '-movflags', '+faststart',  # 优化流媒体播放
            #     '-y',  # 覆盖输出文件
            #     output_file
            # ]
            #linux服务器
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-c:v', 'libx264',  # 视频编码器
                '-preset', 'medium',
                '-crf', '23',
                '-vf', f"scale={res_config['width']}:{res_config['height']}",
                '-b:v', res_config['bitrate'],
                '-maxrate', res_config['bitrate'],
                '-bufsize', str(int(res_config['bitrate'].rstrip('k')) * 2) + 'k',
                '-c:a', 'aac',  # 音频编码器
                '-strict', '-2',  # <--- 关键修改：允许使用实验性的 AAC 编码器
                '-b:a', res_config['audio_bitrate'],
                '-movflags', '+faststart',
                '-y',
                output_file
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True)
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"      ✓ {res_name}: {size_mb:.2f} MB")
                transcoded_files.append({
                    'resolution': res_name,
                    'path': output_file,
                    'size': os.path.getsize(output_file)
                })
            except subprocess.CalledProcessError as e:
                print(f"      ✗ {res_name} 转码失败")

        return transcoded_files
    def generate_hls(self, input_path, output_dir, base_name):
        HLS_SEGMENT_TIME = 10  # 每个 TS 分片的秒数
        """生成 HLS 自适应流"""
        print(f"    生成 HLS...")

        hls_dir = os.path.join(output_dir, f"{base_name}_hls")
        os.makedirs(hls_dir, exist_ok=True)

        master_playlist = os.path.join(hls_dir, "master.m3u8")

        # 构建 ffmpeg 命令 (多码率 HLS)
        # cmd = [
        #     'ffmpeg',
        #     '-i', input_path,
        #     '-c:v', 'libx264',
        #     '-preset', 'medium',
        #     '-crf', '23',
        #     '-c:a', 'aac',
        #     '-b:a', '128k',
        #     '-f', 'hls',
        #     '-hls_time', str(HLS_SEGMENT_TIME),
        #     '-hls_playlist_type', 'vod',
        #     '-hls_segment_filename', os.path.join(hls_dir, f'{base_name}_%03d.ts'),
        #     '-master_pl_name', 'master.m3u8',
        #     os.path.join(hls_dir, f'{base_name}.m3u8')
        # ]
        #Linux
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-strict', '-2',  # 修复实验性 aac 问题
            '-b:a', '128k',
            '-f', 'hls',
            '-hls_time', str(HLS_SEGMENT_TIME),
            '-hls_list_size', '0',
            '-hls_playlist_type', 'vod',
            # 删除了 -hls_playlist_type 和 -master_pl_name，因为 2.8 版本不支持
            '-hls_segment_filename', os.path.join(hls_dir, f'{base_name}_%03d.ts'),
            os.path.join(hls_dir, 'playlist.m3u8')
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)

            # 统计生成的文件
            hls_files = [f for f in os.listdir(hls_dir) if f.endswith(('.m3u8', '.ts'))]
            print(f"      ✓ HLS 生成完成 ({len(hls_files)} 个文件)")

            return hls_dir, hls_files
        except subprocess.CalledProcessError as e:
            print(f"      ✗ HLS 生成失败")
            return None, []

    def upload_to_b2_video(self, local_path, b2_path, file_metadata=None):
        key_in_bucket = b2_path.replace("\\", "/")
        logger.error("正在上传")
        bucket = B2.get_b2_bucket(self)
        res=bucket.upload_local_file(
            local_file=local_path,
            file_name=key_in_bucket,
            file_info=file_metadata or {}
        )
        logger.error(res)
        return True
        # except Exception as e:
        #     print(f"      ✗ 上传失败: {e}")
        #     return False

    def force_convert_to_mp3(self,input_path, bitrate="128k"):
        """
        使用 pydub 强制解码并重新编码，成功后覆盖原文件
        """
        if not os.path.exists(input_path):
            print(f"找不到文件: {input_path}")
            return None

        # 获取不带后缀的文件名
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.mp3"

        try:
            print(f"正在深度解码: {input_path} ...")

            # 自动识别格式并加载 (pydub 内部会调用 ffmpeg 尝试各种解码器)
            audio = AudioSegment.from_file(input_path)

            # 导出为 MP3
            print(f"正在重新编码为 MP3...")
            audio.export(output_path, format="mp3", bitrate=bitrate,parameters=["-ar", "44100", "-ac", "2"])

            # 检查是否成功生成了新文件
            if os.path.exists(output_path):
                # 如果原文件不是 .mp3，或者文件名不同，则删除原文件
                if os.path.abspath(input_path) != os.path.abspath(output_path):
                    os.remove(input_path)
                    print(f"原文件已替换。")

                print(f"转换成功: {output_path}")
                return output_path

        except Exception as e:
            print(f"转换最终失败: {e}")
            return None

    def download_and_convert_audio(self, url, target_bitrate="128k"):
        # 1. 从 URL 获取文件名
        original_filename = url.split('/')[-1]
        base_name = os.path.splitext(original_filename)[0]
        temp_download = f"static/upload/tmp/temp_{original_filename}"
        output_mp3 = f"static/upload/tmp/{base_name}_128k.mp3"

        try:
            # 2. 下载音频文件
            print(f"正在下载音频: {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status()  # 检查下载是否成功

            with open(temp_download, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # 3. 使用 pydub 进行“强力”转换
            # pydub 对处理你遇到的 'junk data' 报错非常有效
            print(f"正在转换并修复音频 (比特率: {target_bitrate})...")
            audio = AudioSegment.from_file(temp_download)

            # 导出为标准 128k MP3
            audio.export(output_mp3, format="mp3", bitrate=target_bitrate,parameters=["-ar", "44100", "-ac", "2"])

            print(f"✅ 转换成功！新文件已生成: {output_mp3}")

            # 4. 清理临时下载的原始文件
            if os.path.exists(temp_download):
                os.remove(temp_download)

            return output_mp3

        except Exception as e:
            print(f"❌ 发生错误: {e}")
            if os.path.exists(temp_download):
                os.remove(temp_download)
            return None