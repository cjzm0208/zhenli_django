from  django import forms
from  django.forms import fields
from  django.forms import widgets
from . import models
from django.db.models import Q

class login_form(forms.Form):
    email=forms.CharField(
        label='邮箱/手机号',
        required=True,
        widget=widgets.TextInput(attrs={'class':'form-control','name':'Email','placeholder':'邮箱/手机号'})
    )
    password=forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class':'form-control','name':'password','placeholder':'密码'})
    )
class RegisterForm(forms.Form):
    password1 = forms.CharField(label="Mot de passe", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Mot de passe'}))
    password2 = forms.CharField(label="Confirmation du mot de passe", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirmation du mot de passe'}))
    email = forms.EmailField(label="Adresse e-mail", widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Adresse e-mail'}))
    nom=forms.CharField(label="Nom", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Nom'}))
    prenom = forms.CharField(label="Pénom", max_length=256,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pénom'}))

class ListChercher(forms.Form):
    def __init__(self ,*args, **kwargs):
        super(ListChercher,self).__init__(*args, **kwargs)
        choix=models.cathegorie.objects.all()
        new_choix=[(0,'全部')]
        for un in choix:
            if(un.parent==0):
                new_choix.append((un.id,un.titre))
                for une in choix:
                    if une.parent==un.id:
                        new_choix.append((une.id,'--'+une.titre))
                        for une3 in choix:
                            if une3.parent==une.id:
                                new_choix.append((une3.id,'------'+une3.titre))

        self.fields["cathegory"].widget.choices = new_choix
    Chercher = forms.CharField(label="搜索", max_length=256,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '搜索'}))
    cathegory=forms.CharField(max_length=255,widget=forms.Select(attrs={'class': 'form-control'}))


class settingForm(forms.Form):
    def __init__(self ,*args, **kwargs):
        super(settingForm,self).__init__(*args, **kwargs)
        choix=models.cathegorie.objects.all()
        new_choix=[]
        for un in choix:
            if(un.parent==0):
                new_choix.append((un.id,un.titre))
                for une in choix:
                    if une.parent==un.id:
                        new_choix.append((une.id,'--'+une.titre))
        self.fields["zhuda_cathe"].widget.choices = new_choix
    index_image_logo = forms.CharField(label="首页大图", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'首页大图'}))
    index_image_logo_lien = forms.CharField(label="首页大图链接",
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '首页大图链接'}))
    index_left_1 = forms.CharField(label="主页 左一图片", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'主页 左一图片'}))
    index_left_1_lien = forms.CharField(label="主页 左一图片链接",
                                            widget=forms.TextInput(
                                                attrs={'class': 'form-control', 'placeholder': '主页 左一图片链接'}))
    index_middle = forms.CharField(label="主页 中部图片", widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'主页 中部图片'}))
    index_middle_lien = forms.CharField(label="主页 中部图片链接",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '主页 中部图片链接'}))
    zhuda_cathe=forms.CharField(label="推荐分类",widget=forms.SelectMultiple(attrs={'class':'form-control'}))