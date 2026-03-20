import json

from django.shortcuts import render, HttpResponse
from . import forms
from . import models
from django.shortcuts import redirect
import hashlib
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
import random
import logging
import pytz
from . import commun
from django.db.models import Q
from django.utils.html import mark_safe
import re
logger = logging.getLogger('django')


def m(request, type, fun):
    is_login = request.session.get('is_login', False)
    user_info = request.session.get('user', False)
    if type == 'index':
        #home
        # tuijian = models.article.objects.order_by('-date_motifier').filter(visuel__isnull=False,
        #                                                                    date_publier__lte=datetime.now())[:5]
        tuijian = models.article.objects.order_by('-date_publier').filter(cathegorie=8)[:5]
        if fun == 'today':
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            today = timezone.now().astimezone(shanghai_tz).strftime('%Y-%m-%d')
            articles = models.article.objects.filter(date_motifier__date=today, visuel__isnull=False).order_by(
                '-date_publier')
        else:
            try:
                date = datetime.strptime(fun, '%Y-%m-%d').date()
                articles = models.article.objects.filter(date_motifier__date=date, visuel__isnull=False).order_by(
                    '-date_publier')
            except ValueError:
                articles = models.article.objects.none()

        #cathegory
        cathegorys = models.cathegorie.objects.filter(observation=1).exclude(id=0)
        new_cathegorys = []
        for un in cathegorys:
            visuel = un.visuel
            images=["https://picsum.photos/id/101/400/400",
                    "https://picsum.photos/id/102/400/400",
                    "https://picsum.photos/id/103/400/400",
                    "https://picsum.photos/id/104/400/400",
                    "https://picsum.photos/id/201/400/400",
                    "https://picsum.photos/id/202/400/400",]
            if not visuel:
                visuel=random.choice(images)
            new_cathegorys.append(
                {"id":un.id,"visuel":visuel,"title":un.titre,"parent":un.parent}
            )
        new_cathegorys=json.dumps(new_cathegorys, ensure_ascii=False)
        #cours
        return render(request, 'mobile/index.html', locals())
    elif type == 'content':
        num=int(fun)
        value = models.article.objects.get(id=num)
        value.visuel = value.visuel.replace("thumbnail", "standard")
        logo = value.visuel.replace("standard-", "icon-")
        # if (value.title != name):
        #     return redirect('/home/')
        models.article.objects.filter(id=value.id).update(lire=value.lire + 1)
        # recents = models.article.objects.order_by('-date_motifier').all()[:5]
        inti = {'type': 'article', 'parent': value.id, 'title': value.title}
        if is_login:
            inti['user_id'] = user_info['id']
        comment = models.comments_input(initial=inti)
        comments = models.comments.objects.filter(parent=num, parent_comment=0)
        for un in comments:
            res = chercher_subcomment(un)
            if not res:
                un = chercher_subcomment(un)
        return render(request,'mobile/content.html', locals())
    elif type == 'cathegory':
        cathegory = models.cathegorie.objects.get(id=fun)
        return render(request,'mobile/articles.html', locals())
    elif type == 'course_details':
        value=models.cours.objects.get(id=fun)
        lessons=models.cours.objects.filter(parent=value.id).values("id","title","fichier_audio")
        lessons=list(lessons)
        return render(request,'mobile/course_details.html', locals())
    elif type == 'lesson':
        return render(request,'mobile/content.html', locals())
    elif type == 'search':
        query = request.GET.get('q', '').strip()
        results = []

        if query:
            # First, search for full query in contenu
            full_query_results = models.article.objects.filter(
                Q(contenu__icontains=query)
            ).distinct()

            # Then, search for individual words in contenu
            words = query.split()
            word_query = Q()
            for word in words:
                word_query |= Q(contenu__icontains=word)

            word_results = models.article.objects.filter(word_query).distinct()

            # Combine results, prioritizing full query matches
            combined_results = list(full_query_results) + [r for r in word_results if r not in full_query_results]

            # Extract and highlight relevant paragraphs
            for result in combined_results:
                paragraphs = result.contenu.split('\n') if result.contenu else []
                matched_paragraphs = []

                # Check for full query matches
                for para in paragraphs:
                    if query.lower() in para.lower() and para.strip():
                        highlighted = re.sub(
                            f'({re.escape(query)})',
                            r'<span class="highlight">\1</span>',
                            para,
                            flags=re.IGNORECASE
                        )
                        matched_paragraphs.append(highlighted)

                # Check for individual word matches
                for para in paragraphs:
                    for word in words:
                        if word.lower() in para.lower() and para.strip() and para not in matched_paragraphs:
                            highlighted = re.sub(
                                f'({re.escape(word)})',
                                r'<span class="highlight">\1</span>',
                                para,
                                flags=re.IGNORECASE
                            )
                            matched_paragraphs.append(highlighted)
                            break  # Avoid duplicate paragraphs

                # Attach matched paragraphs to the result
                if matched_paragraphs:
                    result.matched_paragraphs = matched_paragraphs
                    results.append(result)

        # Paginate results
        paginator = Paginator(results, 20)  # 20 items per page
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'query': query,
            'page_obj': page_obj,
        }
        return render(request,'mobile/search.html', locals())
    elif type == 'wx':
        return render(request, 'mobile/wx.html', locals())

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