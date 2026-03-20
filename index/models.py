from django.db import models
from django.forms import ModelForm
from django.forms import widgets
from collections import OrderedDict

from  django import forms
# Create your models here.
tous_role = [
    (0, "全局管理员"),
    (5, "管理员"),
    (10, "负责人"),
    (15, "老师"),
    (20, "订阅者"),
    (25, "被屏蔽"),
]
tous_etat=(
    ("Religieux(se)", "Religieux(se)"),
    ("Diacre", "Diacre"),
    ("Prêtre", "Prêtre"),
    ("Individuel", "Individuel"),
    ("Famille", "Famille"),
    ("Parent seul", "Parent seul")
)
oui_non=[
    (1,"是"),
    (0,"否")
]
sex=[
    ("男","男"),
    ("女","女")
]
class compte(models.Model):
    email = models.CharField(max_length=256,unique=True,verbose_name='邮箱/手机号')
    mots_passe = models.CharField(max_length=256,verbose_name='密码')
    refaire_motes_passe	 = models.CharField(max_length=256,verbose_name='确认密码')
    prenom = models.CharField(max_length=50,null=True,verbose_name='姓名')
    role = models.IntegerField(choices=tous_role,default=20,blank=True)
    etat = models.IntegerField(null=True,choices=tous_etat,blank=True)
    sex = models.CharField(max_length=10, null=True, verbose_name="性别", choices=sex,blank=True)
    etat_vie = models.CharField(max_length=50,null=True, choices=tous_etat,verbose_name='个人情况')
    naissance = models.DateField(null=True,blank=True, verbose_name='生日')
    adresse = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址')
    saintnom = models.CharField(max_length=255, null=True, blank=True, verbose_name='圣名')
    ville = models.CharField(max_length=255, null=True, blank=True, verbose_name='城市')
    pays = models.CharField(max_length=255, null=True, blank=True, verbose_name='国家')
    Tel = models.CharField(max_length=50,null=True,blank=True,verbose_name='电话')
    visuel=models.CharField(max_length=255,null=True,blank=True)
    Ip = models.CharField(max_length=50,null=True,blank=True)
    equipement = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)
    has_confirmed = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.email

class moncompte(ModelForm):  # 继承ModelForm类
    def __init__(self,user_info,*args,**kwargs):
        super(moncompte,self).__init__(*args,**kwargs)
        les_roles = [
            (0, "全局管理员"),
            (5, "管理员"),
            (10, "负责人"),
            (15, "老师"),
            (20, "订阅者"),
        ]
        if(user_info['role']==0):
            les_roles = [
                (0, "全局管理员"),
                (5, "管理员"),
                (10, "负责人"),
                (15, "老师"),
                (20, "订阅者"),
            ]
        else:
            for i in range(len(les_roles) - 1, -1, -1):
                if les_roles[i][0] <= user_info['role']:
                    les_roles.pop(i)
        self.fields['role'].widget.choices=les_roles
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
    class Meta:
        model = compte  # 具体要操作那个模型
        # exclude = ['mots_passe','refaire_motes_passe','parent','date_creer','date_motifier','has_confirmed','etat_vie','etat','visuel','Ip','equipement']
        fields = ['email','prenom','role','sex','naissance','Tel','pays','ville','adresse','user_id','user_name']
        widgets = {
            'email': widgets.TextInput(attrs={'class':'form-control','placeholder':'邮箱/手机号','readonly':'readonly'}),
            'prenom': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名','readonly':'readonly'}),
            'sex':widgets.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'role': widgets.Select(attrs={'class': 'form-control', 'placeholder': '权限'}),
            'Tel': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '电话', 'readonly': 'readonly'}),
            'etat_vie': widgets.Select(attrs={'class': 'form-control', 'placeholder': 'État de vie'}),
            'naissance': widgets.DateInput(attrs={'class': 'form-control', 'placeholder': '城市','readonly':'readonly'}),
            'ville': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '地址', 'readonly': 'readonly'}),
            'pays': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '国家','readonly':'readonly'}),
            'adresse': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '地址','readonly':'readonly'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class index_login_input(ModelForm):
    class Meta:
        model = compte  # 具体要操作那个模型
        # exclude = ['parent','date_creer','date_motifier','etat','visuel','nom_maison','role','vip','date_vip','user_id','user_name','responsable','has_confirmed','nom_communaute','Ip','equipement','forfaits','pourcentage','payeur']
        fields = ['email', 'mots_passe','refaire_motes_passe','prenom']
        widgets = {
            'email': widgets.TextInput(attrs={'class':'form-control','placeholder':'邮箱'}),
            'prenom': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'}),
            # 'nom': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'mots_passe': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
            'refaire_motes_passe': widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'}),
            # 'sex':widgets.Select(attrs={'class': 'form-control'}),
            # 'etat_vie': widgets.Select(attrs={'class': 'form-control', 'placeholder': 'État de vie'}),
            # 'naissance': widgets.DateInput(attrs={'class': 'form-control date_input', 'placeholder': 'Naissance'}),
            # 'pays': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pays'}),
            # 'ville': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}),
            # 'adresse': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse'}),
            # 'code_postal': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code Postal',}),
            # 'maison': widgets.Select(attrs={'class': 'form-control'}),
            # 'communaute': widgets.Select(attrs={'class': 'form-control'}),
            # 'Tel': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tel'}),
        }
class cathegorie(models.Model):
    titre = models.CharField(max_length=255,verbose_name='名称', null=True)
    parent = models.IntegerField(verbose_name='父分类',default=0,blank=True)
    note = models.TextField(verbose_name='标记', null=True,blank=True)
    original = models.IntegerField(null=True,blank=True)
    visuel = models.CharField(max_length=255, verbose_name='封面', null=True, blank=True)
    ordre = models.IntegerField(null=True, blank=True,default=0)
    observation = models.IntegerField(choices=oui_non, verbose_name='显示', default=1)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)

class cathegorie_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(cathegorie_input,self).__init__(*args,**kwargs)
        new_cathegorie=[(0,'-------')]
        tous=cathegorie.objects.all()
        for un in tous:
            if un.parent==0:
                new_cathegorie.append((un.id,un.titre))
                for une in tous:
                    if une.parent==un.id:
                        new_cathegorie.append((une.id,'--'+une.titre))
        # tous=cathegorie.objects.filter(parent=0).values_list('id','titre')
        # tous=list(tous)
        # tous.insert(0,(0,'-------'))

        self.fields['parent'].widget.choices= new_cathegorie
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
    class Meta:
        model = cathegorie  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_motifier','original']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'note': widgets.Textarea(attrs={'class': 'form-control','placeholder': 'Contenu','rows':5}),
            'parent': widgets.Select(attrs={'class': 'form-control', 'placeholder': '父分类'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'titre': widgets.TextInput(attrs={'class': 'form-control'}),
            'visuel': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Visuel'}),
            'ordre': widgets.NumberInput(attrs={'class': 'form-control'}),
            'observation': widgets.RadioSelect(attrs={}),
            'original': widgets.NumberInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class pages(models.Model):
    title = models.CharField(max_length=255, verbose_name='Titre',null=True)
    contenu = models.TextField(verbose_name='Contenu',null=True)
    observation = models.IntegerField(choices=oui_non,verbose_name='Publier',default=1)
    fichier_audio= models.CharField(max_length=255, verbose_name='Audio',null=True,blank=True)
    fichier_video = models.CharField(max_length=255, verbose_name='Video', null=True, blank=True)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)
    # def __str__(self):
    #     return self.maison

class pages_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(pages_input,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
    class Meta:
        model = pages  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_motifier', 'fichier_audio']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'id':'contenu', 'placeholder': 'Contenu','rows':5}),
            'observation': widgets.RadioSelect(attrs={}),
            'fichier_audio': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Audio'}),
            'fichier_video': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Vidéo'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class article(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题',null=True)
    color = models.CharField(max_length=50, verbose_name='标题颜色', null=True,blank=True)
    contenu = models.TextField(verbose_name='内容',null=True,blank=True)
    description = models.TextField(verbose_name='简单描述', null=True, blank=True)
    observation = models.IntegerField(choices=oui_non,verbose_name='发布',default=1)
    cathegorie = models.ManyToManyField(cathegorie,verbose_name='分类')
    visuel = models.CharField(max_length=255, verbose_name='封面', null=True, blank=True)
    fichier_audio= models.CharField(max_length=255, verbose_name='音频',null=True,blank=True)
    duration = models.IntegerField(verbose_name='音频时长', default=0)
    fichier_video = models.CharField(max_length=255, verbose_name='视频', null=True, blank=True)
    date_publier = models.DateTimeField(auto_now=True,verbose_name='修改时间', null=True,blank=True)
    lire = models.IntegerField(null=True,blank=True,default=0)
    new_contenu = models.TextField(verbose_name='新内容', null=True, blank=True,default="[]")
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(verbose_name='发布时间',null=True,blank=True)
    frequency_date = models.CharField(max_length=20, verbose_name='重复时间', default=0, null=True, blank=True, )
    # def __str__(self):
    #     return self.title

class article_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(article_input,self).__init__(*args,**kwargs)
        cathegories=cathegorie.objects.order_by('ordre','id').all()
        new_cathegories=[]
        for un in cathegories:
            if un.parent==0:
                new_cathegories.append((un.id,un.titre))
                for une in cathegories:
                    if une.parent==un.id:
                        new_cathegories.append((une.id, '---'+une.titre))
                        for une3 in cathegories:
                            if une3.parent==une.id:
                                new_cathegories.append((une3.id, '-------'+une3.titre))
        self.fields['cathegorie'].widget.choices=new_cathegories
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
    class Meta:
        model = article  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_publier']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'color': widgets.TextInput(attrs={'class': 'form-control my-colorpicker1 colorpicker-element', 'placeholder': '标题颜色'}),
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'id':'contenu', 'placeholder': 'Contenu','rows':5}),
            'description': widgets.Textarea(
                attrs={'class': 'form-control', 'placeholder': '简要', 'rows': 3}),
            'observation': widgets.RadioSelect(attrs={}),
            'visuel': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Visuel'}),
            'date_motifier': widgets.DateInput(format=('%Y-%m-%d %H:%M:%S'), attrs={'class': 'form-control datetime_input'}),
            'cathegorie': widgets.SelectMultiple(attrs={'class': 'form-control modal_cathegorie', 'placeholder': '分类'}),
            'fichier_audio': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Audio'}),
            'duration': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'fichier_video': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Vidéo'}),
            'frequency_date': widgets.DateInput(
                                               attrs={'class': 'form-control date_mm_dd'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'lire': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'new_contenu': widgets.HiddenInput(
                attrs={'class': 'form-control', 'placeholder': 'Contenu', 'rows': 5}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class pray(models.Model):
    contenu = models.TextField(verbose_name='内容',null=True,blank=True)
    payer = models.IntegerField(null=True,blank=True,default=0)
    louer = models.IntegerField(null=True, blank=True, default=0)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)
    # def __str__(self):
    #     return self.title

class dossiers(models.Model):
    nom_org=models.CharField(max_length=255, verbose_name='Nom',null=True)
    nom = models.CharField(max_length=255, verbose_name='Nom', null=True)
    type = models.CharField(max_length=255, verbose_name='Nom', null=True)
    duration = models.FloatField(null=True)
    lien = models.CharField(max_length=255, verbose_name='Nom', null=True)
    stantard = models.CharField(max_length=255, verbose_name='Nom', null=True)
    thumb = models.CharField(max_length=255, verbose_name='Nom', null=True)
    file = models.FileField(upload_to = 'media/%Y/%m/%d/')
    date_creer = models.DateTimeField(auto_now_add=True, verbose_name='Date creer', null=True)
    date_motifier = models.DateTimeField(auto_now=True, verbose_name='Date motifier', null=True)
    user_id = models.IntegerField(null=True,verbose_name='Nom')
    maison = models.IntegerField(null=True, verbose_name='Nom')

class cathegorie_cours(models.Model):
    titre = models.CharField(max_length=255,verbose_name='名称', null=True)
    parent = models.ForeignKey('cathegorie_cours', on_delete=models.CASCADE, null=True, default=1,blank=True)
    note = models.TextField(verbose_name='标记', null=True,blank=True)
    original = models.IntegerField(null=True,blank=True)
    ordre = models.IntegerField(null=True, blank=True,default=0)
    visuel = models.CharField(max_length=255, verbose_name='封面', null=True, blank=True)
    observation = models.IntegerField(choices=oui_non, verbose_name='显示', default=1)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)

class cathegorie_cours_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(cathegorie_cours_input,self).__init__(*args,**kwargs)   #这里要修改
        cathegories = [(1,"----")]
        tous = cathegorie_cours.objects.exclude(id=1)
        for un in tous:
            if un.parent.id == 1:
                cathegories.append((un.id, un.titre))
                for une in tous:
                    if une.parent.id == un.id:
                        cathegories.append((une.id, "-" + une.titre))
        self.fields['parent'].widget.choices= cathegories
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
    class Meta:
        model = cathegorie_cours  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_motifier','original']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'note': widgets.Textarea(attrs={'class': 'form-control','placeholder': 'Contenu','rows':5}),
            'parent': widgets.Select(attrs={'class': 'form-control', 'placeholder': '父分类'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'titre': widgets.TextInput(attrs={'class': 'form-control'}),
            'visuel': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Visuel'}),
            'ordre': widgets.NumberInput(attrs={'class': 'form-control'}),
            'observation': widgets.RadioSelect(attrs={}),
            'original': widgets.NumberInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class cours(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题', null=True)
    contenu = models.TextField(verbose_name='内容', null=True, blank=True)
    description = models.TextField(verbose_name='简单描述', null=True, blank=True)
    observation = models.IntegerField(choices=oui_non, verbose_name='发布', default=1)
    ordre = models.IntegerField(null=True, blank=True, default=0)
    parent = models.IntegerField(null=True, blank=True, default=0)
    visuel = models.CharField(max_length=255, verbose_name='Visuel', null=True, blank=True)
    cathegorie = models.ForeignKey('cathegorie_cours', on_delete=models.CASCADE,verbose_name='分类',null=True, default=1, blank=True)
    fichier_audio = models.CharField(max_length=255, verbose_name='音频', null=True, blank=True)
    duration = models.IntegerField(verbose_name='音频时长', default=0)
    fichier_video = models.CharField(max_length=255, verbose_name='视频', null=True, blank=True)
    lire = models.IntegerField(null=True, blank=True, default=0)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True, verbose_name='Date creer', null=True)
    date_motifier = models.DateTimeField(auto_now=True, verbose_name='Date motifier', null=True)

class cours_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(cours_input,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
        cathegories=[]
        tous = cathegorie_cours.objects.exclude(id=1)
        for un in tous:
            if un.parent.id ==1:
                cathegories.append((un.id,un.titre))
                for une in tous:
                    if une.parent.id == un.id:
                        cathegories.append((une.id,"-"+une.titre))
        self.fields['cathegorie'].widget.choices = cathegories
    class Meta:
        model = cours  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_motifier']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'id':'contenu', 'placeholder': 'Contenu','rows':5}),
            'description': widgets.Textarea(
                attrs={'class': 'form-control', 'placeholder': '简要', 'rows': 3}),
            'observation': widgets.RadioSelect(attrs={}),
            'cathegorie': widgets.Select(attrs={'class': 'form-control'}),
            'ordre': widgets.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Visuel'}),
            'visuel': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Visuel'}),
            'parent': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': '分类'}),
            'fichier_audio': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Audio'}),
            'duration': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'fichier_video': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Vidéo'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'lire': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class live(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题', null=True)
    contenu = models.TextField(verbose_name='内容', null=True, blank=True)
    description = models.TextField(verbose_name='简单描述', null=True, blank=True)
    observation = models.IntegerField(choices=oui_non, verbose_name='发布', default=1)
    visuel = models.CharField(max_length=255, verbose_name='Visuel', null=True, blank=True)
    live_video = models.CharField(max_length=255, verbose_name='直播地址', null=True, blank=True)
    relive_video = models.CharField(max_length=255, verbose_name='回播地址', null=True, blank=True)
    livepushurl = models.CharField(max_length=255, verbose_name='livepushurl', null=True, blank=True)
    logininfokey = models.CharField(max_length=255, verbose_name='logininfokey', null=True, blank=True)
    start = models.DateTimeField(verbose_name='开始时间', null=True)
    end = models.DateTimeField(verbose_name='结束时间', null=True)
    professeur = models.ForeignKey(compte, on_delete=models.CASCADE, null=True,default=1)
    lire = models.IntegerField(null=True, blank=True, default=0)
    user_id = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
    date_creer = models.DateTimeField(auto_now_add=True, verbose_name='Date creer', null=True)
    date_motifier = models.DateTimeField(auto_now=True, verbose_name='Date motifier', null=True)

class live_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(live_input,self).__init__(*args,**kwargs)
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
        self.fields['user_name'].widget.attrs['value'] = user_info['nom']
        profeseurs=compte.objects.filter(role__gte=15).values_list('id','prenom')
        self.fields['professeur'].widget.choices = profeseurs
    class Meta:
        model = live  # 具体要操作那个模型
        exclude = [ 'date_creer', 'date_motifier']
        # fields = ['email', 'prenom', 'nom','nom_maison']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '标题'}),
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'id':'contenu', 'placeholder': '内容','rows':5}),
            'description': widgets.Textarea(
                attrs={'class': 'form-control', 'placeholder': '简要', 'rows': 3}),
            'observation': widgets.RadioSelect(attrs={}),
            'visuel': widgets.HiddenInput(attrs={'class': 'form-control', 'placeholder': '封面'}),
            'start': widgets.TextInput(attrs={'class': 'form-control datetime_input', 'placeholder': '开始时间'}),
            'end': widgets.TextInput(attrs={'class': 'form-control datetime_input', 'placeholder': '结束时间'}),
            'live_video': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '直播地址'}),
            'relive_video': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': '回播地址'}),
            'livepushurl': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'livepushurl'}),
            'logininfokey': widgets.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'logininfokey'}),
            'professeur': widgets.Select(attrs={'class': 'form-control', 'placeholder': '老师'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'lire': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class feedback(models.Model):
    contenu = models.TextField(verbose_name='内容',null=True,blank=True)
    email = models.CharField(max_length=255, verbose_name='邮箱', null=True)
    parent = models.IntegerField(verbose_name='文章id', null=True, default=0)
    user_name = models.CharField(max_length=255, null=True,blank=True)
    user_id = models.IntegerField(null=True,blank=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    date_motifier = models.DateTimeField(auto_now=True,verbose_name='Date motifier',null=True)

class feedback_input(ModelForm):
    class Meta:
        model = feedback  # 具体要操作那个模型
        fields = ['contenu','parent','user_id']
        widgets = {
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu','rows':5}),
            'observation': widgets.RadioSelect(attrs={}),
            'parent': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }
class favorise(models.Model):
    type = models.CharField(max_length=255, verbose_name='标题', null=True)
    post_id = models.IntegerField(null=True)
    user_id = models.IntegerField(null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)

class comments(models.Model):
    type = models.CharField(max_length=255, verbose_name='类型',null=True,default='article')
    title = models.CharField(max_length=255, verbose_name='标题', null=True ,blank=True)
    contenu = models.TextField(verbose_name='内容',null=True,blank=True)
    observation = models.IntegerField(choices=oui_non,verbose_name='发布',default=1,blank=True)
    parent = models.IntegerField(verbose_name='文章id',null=True,default=0)
    ordre = models.IntegerField(verbose_name='显示顺序', default=0, blank=True)
    parent_comment = models.IntegerField(verbose_name='回复', default=0,blank=True)
    user_id = models.ForeignKey('compte',on_delete=models.CASCADE, null=True,default=1)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)
    # def __str__(self):
    #     return self.title
class comments_input(ModelForm):
    class Meta:
        model = comments  # 具体要操作那个模型
        fields = ['contenu','parent','parent_comment','user_id','ordre','title','type']
        widgets = {
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '内容','rows':5}),
            'observation': widgets.RadioSelect(attrs={}),
            'ordre': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '显示顺序'}),
            'parent': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'type': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'title': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'parent_comment': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class verifi_code(models.Model):
    type = models.IntegerField(verbose_name='类型', null=True,default=0)
    tel = models.CharField(max_length=255, verbose_name='手机号',null=True)
    code = models.CharField(max_length=255, verbose_name='验证码', null=True)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)

class setting(models.Model):
    key = models.CharField(max_length=255, verbose_name='关键字', null=True)
    contenu = models.TextField(verbose_name='内容', null=True)
    note = models.TextField(verbose_name='链接', null=True)
    user_id = models.IntegerField(null=True)
    date_creer = models.DateTimeField(auto_now_add=True, verbose_name='Date creer', null=True)
    date_motifier = models.DateTimeField(auto_now=True, verbose_name='Date motifier', null=True)
class setting_input(ModelForm):
    class Meta:
        model = setting  # 具体要操作那个模型
        fields = ['key','contenu','note','user_id']
        widgets = {
            'contenu': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu','rows':5}),
            'note': widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu','rows':5}),
            'key': widgets.TextInput(attrs={'class': 'form-control','readonly':'readonly'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }

class sg_bibleBook(models.Model):
    name = models.CharField(max_length=255, verbose_name='卷名',null=True)
    brev = models.CharField(max_length=255, verbose_name='简写', null=True)
    mark = models.CharField(max_length=10, verbose_name='公共标记', null=True, blank=True,unique=True)
    chapitre = models.TextField(verbose_name='章节', null=True, blank=True)

class sg_bibleBook_input(ModelForm):
    class Meta:
        model = sg_bibleBook  # 具体要操作那个模型
        fields = ['name','brev','mark']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'brev': widgets.TextInput(attrs={'class': 'form-control'}),
            'mark': widgets.TextInput(attrs={'class': 'form-control'}),
        }

class sg_bible(models.Model):
    date = models.DateTimeField(verbose_name='日期', null=True, blank=True)
    contenu = models.TextField(verbose_name='内容', null=True, blank=True)
    book = models.ForeignKey('sg_bibleBook', on_delete=models.CASCADE, null=True, default=1)
    livre = models.CharField(max_length=20, verbose_name='标记', null=True)
    chapitre = models.IntegerField(verbose_name='章', null=True)
    partie = models.IntegerField(verbose_name='节', null=True)
    paragraph = models.IntegerField(verbose_name='分段', null=True)
    commun = models.CharField(max_length=100, verbose_name='公共参数', null=True,blank=True)

class sg_bible_input(ModelForm):
    class Meta:
        model = sg_bible  # 具体要操作那个模型
        fields = ['chapitre','contenu']
        widgets = {
            'chapitre': widgets.TextInput(attrs={'class': 'form-control'}),
            'contenu': widgets.TextInput(attrs={'class': 'form-control'}),
        }

class sg_lecture(models.Model):
    impair = models.IntegerField(verbose_name="单双年",null=True,blank=True,choices=[(1,"单数年"),(0,"双数年")])
    abc = models.IntegerField(verbose_name="甲乙丙", null=True, blank=True,choices=[(0,"A"),(1,"B"),(2,"C")])
    name = models.CharField(max_length=255,verbose_name="名称", null=True, blank=True)
    fete = models.IntegerField(verbose_name="节庆日", null=True, blank=True,choices=[(0,"纪"),(1,"节"),(2,"庆")])
    sign = models.CharField(max_length=255, verbose_name="标记", null=True, blank=True)
    messe = models.TextField( verbose_name="弥撒", null=True, blank=True)
    info = models.TextField(verbose_name='介绍', null=True, blank=True)
    lecture = models.TextField(verbose_name='诵读', null=True, blank=True)
    laudes = models.TextField(verbose_name='早祷', null=True, blank=True)
    tierce = models.TextField(verbose_name='午前', null=True, blank=True)
    sexte = models.TextField(verbose_name='午时', null=True, blank=True)
    none = models.TextField(verbose_name='午后', null=True, blank=True)
    vepre = models.TextField(verbose_name='晚祷', null=True, blank=True)
    complies = models.TextField(verbose_name='夜祷', null=True, blank=True)

class sg_lecture_input(ModelForm):
    class Meta:
        model = sg_lecture  # 具体要操作那个模型
        exclude = []
        widgets = {
            'impair': widgets.Select(attrs={'class': 'form-control'}),
            'abc': widgets.Select(attrs={'class': 'form-control'}),
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'fete': widgets.Select(attrs={'class': 'form-control'}),
            'sign': widgets.TextInput(attrs={'class': 'form-control'}),
            'messe': widgets.Textarea(attrs={'class': 'form-control tinymce','rows':10}),
            'info': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'lecture': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'laudes': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'tierce': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'sexte': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'messe': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'none': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'vepre': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
            'complies': widgets.Textarea(attrs={'class': 'form-control tinymce', 'rows': 10}),
        }

class app_index(models.Model):
    title=models.CharField(max_length=255, verbose_name='主题标题', null=True, blank=True)
    cathegory = models.ForeignKey('cathegorie', on_delete=models.CASCADE, null=True, default=0,verbose_name="分类")
    type = models.CharField(max_length=255, verbose_name='类型', null=True, choices=[('single','单次显示'),('loops','循环'),('new','最新'),('time','时间显示'),('time_new','时间显示如无显示最新')],default='single')
    days = models.IntegerField(verbose_name='显示几天/显示几条',null=True,default=1)
    parent=models.ForeignKey('app_index', on_delete=models.CASCADE, null=True, default=0,verbose_name='主题',)
    user_id = models.ForeignKey('compte',on_delete=models.CASCADE, null=True,default=1)
    date_creer = models.DateTimeField(auto_now_add=True,verbose_name='Date creer',null=True)

class app_index_input(ModelForm):
    def __init__(self,user_info,*args,**kwargs):
        super(app_index_input,self).__init__(*args,**kwargs)
        new_cathegorie=[]
        tous=cathegorie.objects.all()
        for un in tous:
            if un.parent==0:
                new_cathegorie.append((un.id,un.titre))
                for une in tous:
                    if une.parent==un.id:
                        new_cathegorie.append((une.id,'--'+une.titre))
        self.fields['cathegory'].widget.choices= new_cathegorie
        parents=app_index.objects.filter(parent=1)
        new_parents=[]
        for un in parents:
            new_parents.append((un.id,un.title))
        self.fields['parent'].widget.choices= new_parents
        self.fields['user_id'].widget.attrs['value'] = user_info['id']
    class Meta:
        model = app_index  # 具体要操作那个模型
        fields = ["parent",'title',"parent",'cathegory','type','days','user_id']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'cathegory': widgets.Select(attrs={'class': 'form-control'}),
            'parent': widgets.Select(attrs={'class': 'form-control'}),
            'type': widgets.Select(attrs={'class': 'form-control'}),
            'days': widgets.NumberInput(attrs={'class': 'form-control'}),
            'user_name': widgets.HiddenInput(attrs={'class': 'form-control'}),
            'user_id': widgets.HiddenInput(attrs={'class': 'form-control'}),
        }
