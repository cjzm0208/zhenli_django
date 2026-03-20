from django import template
from index import forms
import random
import time
import datetime
import json
register = template.Library()
from django.utils.safestring import mark_safe

@register.filter
def replace(value,text):
    """
    Replace all occurrences of a substring in the value.
    Usage: {{ value|replace:"old,new" }}
    """
    # old, new = arg.split(',')
    return value.replace(text,"")
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key,None)

@register.filter
def get_item_verse(dictionary, key):
    return dictionary.get(key,True)

@register.filter
def get_input(inputs, key):
    return inputs[key]

@register.filter
def get_label(inputs, key):
    return inputs[key].label

@register.filter
def get_error(inputs, key):
    return inputs[key].errors

@register.filter
def row_before(dictionary, key):
    class1=dictionary.get(key,[True, 'col', True])
    return class1[0]

@register.filter
def col_before(dictionary, key):
    class1=dictionary.get(key,[True, 'col', True])
    return class1[1]

@register.filter
def row_after(dictionary, key):
    class1=dictionary.get(key,[True, 'col', True])
    return class1[2]

@register.filter
def tag_special(dic, key):
    if(key=='tagrole'):
        tous_role = {
            0: "Admin",
            5:"Communauté",
            10: "Maison",
            15: "Responsable",
            20: "Abonné",
        }
        return tous_role.get(dic['role'],'Abonné')

@register.filter
def gauche(dictionary, key):
    res=True
    for i in dictionary:
        if (i == key):
            res&=False
    return res

@register.filter
def droit(dictionary, key):
    for i in dictionary:
        if (i == key):
            return True

@register.simple_tag
def my_tag(a,b,c):
    obj = forms.mon_role(2)
    return obj

@register.simple_tag
def spcical_before(type):
    if(type=='button_audio'):
        res='<div class="input-group">'
        return mark_safe(res)
    elif type=='button_video':
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=='button_visuel':
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=="inscri_parent":
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=="question":
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=="setting":
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=="repas":
        res = '<div class="row">'
        return mark_safe(res)
    elif type=="produitSort":
        res = '''<div class="row">'''
        return mark_safe(res)
    elif type=='button_pdf':
        res = '<div class="input-group">'
        return mark_safe(res)
    elif type=='button_xml':
        res = '<div class="input-group">'
        return mark_safe(res)
@register.simple_tag
def spcical_after(type):
    if(type=='button_audio'):
        res='''<span class="input-group-append">
                    <button type="button" class="btn btn-info btn-flat dossier" pour="fichier_audio" id="dossier" dossier_type="audio" data-toggle="modal" data-target="#modal-document">Audio</button>
                  </span>
                </div>
                <div id="audio_prevoir" style="margin-top: 1rem;"></div>'''
        return mark_safe(res)
    elif type=='button_video':
        res = '''<span class="input-group-append">
                            <button type="button" class="btn btn-info btn-flat dossier" pour="fichier_video" id="dossier" dossier_type="video" data-toggle="modal" data-target="#modal-document">Vidéo</button>
                          </span>
                        </div>
                        <div id="video_prevoir" style="margin-top: 1rem;"></div>'''
        return mark_safe(res)
    elif type=='button_visuel':
        res = '''
        <div class="visuel"><img width=80% id="img_visuel" src=""> <button type="button" class="btn btn-info btn-flat dossier" id="dossier" pour="visuel"  dossier_type="image" data-toggle="modal" data-target="#modal-document">Visuel</button></div>
        </div>'''
        return mark_safe(res)
    elif type=="inscri_parent":
        res = '''<div><button type="button" class="btn btn-info" id="ajouter_parent">Ajouter une persone</button></div>
                      </div><div id="parents" style='width:100%'><table class="table table-bordered"><thead>
<tr><th>Chambres</th><th>Prénom</th><th>Nom</th><th>Realtion</th><th>Naissance</th><th>#</th></tr></thead><tbody id="parents_body"></tbody></table></div>'''
        return mark_safe(res)
    elif type=="question":
        res = '''</div>
        <div id="Repondre"></div>
        <button type="button" class="btn btn-info Repondre" id="Repondre">Repondre</button>
               '''
        return mark_safe(res)
    elif type=='setting':
        res = '''<span class="input-group-append">
                            <div class="input-group-text"><i class="fas fa-cog"></i></div>
                          </span>
                        </div>
                        <div id="video_prevoir" style="margin-top: 1rem;"></div>'''
        return mark_safe(res)
    elif type=='repas':
        res = ''' <div id="repas" style="width:100%"><table class="table table-bordered"><thead>
<tr><th>Petit-déjeuner</th><th>Déjeuner</th><th>Dîner</th></tr></thead><tbody id="repas_body"></tbody></table></div></div>'''
        return mark_safe(res)
    elif type=="produitSort":
        res = '''
        <label for="id_sorte" class="col-sm-1 col-form-label">Sorte:</label>
  <div class="col" id="sorte_groupe">
      <div class="form-group row">
             <div class="input-group col-sm-12">
                <input type="text" name="sorte" class="form-control" placeholder="Sorte" maxlength="255" id="id_sorte">
                <span class="input-group-append">
                    <img  height="38rem"  style="margin-left: 1rem">
                    <input type="hidden" name="sorteimage" class="form-control" placeholder="Image" maxlength="255" id="id_sorteimage" >
                    <button type="button" class="btn btn-info btn-flat dossier" id="dossier" pour="sorteimage" dossier_type="image" data-toggle="modal" data-target="#modal-document" style="margin-left: 1rem">Image</button>
                <h4 class="text-primary"><i class="far fa-trash-alt" style="margin-left:1rem"></i></h4></span>
             </div>
         </div>
</div>

         </div>
         <div class="row">
    <button type="button" class="btn-sm btn-primary" id="ajouter_sorte" style="margin-left: 0.5rem" >Ajouter</button>
</div>
        '''
        return mark_safe(res)
    elif type=='button_pdf':
        res = '''<span class="input-group-append">
                            <button type="button" class="btn btn-info btn-flat dossier" pour="fichier_pdf" id="dossier" dossier_type="pdf" data-toggle="modal" data-target="#modal-document">Pdf</button>
                          </span>
                        </div>'''
        return mark_safe(res)
    elif type=='button_xml':
        res = '''<span class="input-group-append">
                            <button type="button" class="btn btn-info btn-flat dossier" pour="fichier_xml" id="dossier" dossier_type="xml" data-toggle="modal" data-target="#modal-document">Xml</button>
                          </span>
                        </div>'''
        return mark_safe(res)

@register.filter
def si_arr(arr,value):
    if value in arr:
        return False
    else:
        return True

@register.simple_tag
def random1():
    return random.randint(0,10000000000000)

@register.filter
def formule_text(key, text):
    if text in key:
        return False
    else:
        return True

@register.filter
def si_key(dic,key):
    if key in dic.keys():
        return True
    else:
        return False

@register.filter
def inscrip_setting_get_item(dictionary, key):
    if dictionary:
        if key in dictionary:
            return dictionary[key]['value']
        else:
            return ''
    else:
        return ''
@register.filter
def inscrip_setting_show(dictionary, key):
    if dictionary:
        if key in dictionary:
            return dictionary[key]['show']
        else:
            return True
    else:
        return True

@register.simple_tag
def parametre_tag(parametre,field):
    if(field in parametre):
        return parametre[field]['tag']
    else:
        return ''

@register.filter
def visuel_imgage(src):
    if src:
        src = src.replace('-thumbnail','')
        return src
    else:
        return ''

@register.filter
def taxe(value,pourcentage):
    if value:
        return value*pourcentage
    else:
        return 0

@register.filter
def detoday(value,date):
    today = datetime.datetime.now()
    dif=today-date
    return dif.days

@register.filter
def page_manque(courant,page):
    value=abs(courant-page)
    return value

@register.simple_tag
def visuel_large(visuel):
    return visuel.replace('thumbnail','standard')



