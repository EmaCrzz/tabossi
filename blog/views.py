import json
import datetime 

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import(
    Post,
    Comment,
    Section,
    Document,
    BlacklistString,
    Avatar,
    Image
)
from .forms import CommentForm


def section_list(request):
    images = Image.objects.filter(post_id=None)
    section_default = Section.objects.get(default=True)
    posts = Post.objects.filter(section=section_default)
    return render(
        request,
        'base.html',
        {
            'posts': posts,
            'images': images,
        }
    )


def posts_sections(request, pk):
    sections = Section.objects.filter(disable=False)
    posts = Post.objects.filter(section=pk).order_by('-published_date')
    return render(request, 'posts/post_list.html', {'posts': posts, 'sections': sections})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comentarios = Comment.objects.filter(post_id=pk)
    documents = Document.objects.filter(post_id=pk)
    form = CommentForm()
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post,
            'comentarios': comentarios,
            'documents': documents,
            'form': form,
        }
    )


def add_comment(request, pk):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST)
        name = request.POST['name']
        text = request.POST['text']
        respuesta = {'status': 'success'}
        if censura(text):
            respuesta['status'] = "error"
            respuesta['errors'] = [{
                'msg': u'No se permiten comentarions ofensivos'
            }]
            return JsonResponse(
                respuesta,
                status=200
            )
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                respuesta,
                status=200
            )
        else:
            respuesta['status'] = u'error'
            respuesta['errors'] = form.errors.as_json()
            return JsonResponse(
                respuesta,
                status=200
            )
    return render(request, 'posts/post_detail.html')


def censura(string):
    value = string.strip().upper()
    match = False
    if BlacklistString.objects.filter(string__iexact=value).exists():
        match = True
        return match
    separadores = ['-','/','|','*','_','?','¡','¿','!','#','$','(',')','=',',','{','}'
        ,'[',']',"'", '"']
    for separador in separadores:
        palabrasUsuario = value.split(separador)
        for palabra in palabrasUsuario:
            if BlacklistString.objects.filter(string__iexact=palabra).exists():
                match = True
                return match
    ofencivas = BlacklistString.objects.all()
    for ofenciva in ofencivas:
        if (value.find(ofenciva.string,0,len(value)) > 0):
            match = True
    return match


def list_comment(request, pk):
    comentarios = Comment.objects.filter(post_id=pk).order_by('-created_date').reverse()
    comentarios_serialized = serializers.serialize('json', comentarios)
    return JsonResponse(comentarios_serialized, safe=False) 


def avatar_list(request):
    cargos = Avatar.objects.all()    
    return render(
        request,
        'gobierno/gobierno.html',
        {'cargos': cargos}
    )


def ordenanzas_list(request):
    if request.method == 'GET' and request.is_ajax():
        respuesta = {'status': 'success'}
        ordenanzas = {}
        data = Document.objects.filter(ordenanza=True).order_by('-published_date')
        for d in data:
            if d.published_date.year in ordenanzas:
                ordenanzas[d.published_date.year].append(
                    {
                        'description': d.description,
                        'published_date': d.published_date.strftime("%d/%m/%Y"),
                        'document': d.document.url
                    }
                )
            else:
                ordenanzas[d.published_date.year] = [{
                    'description': d.description,
                    'published_date': d.published_date.strftime("%d/%m/%Y"),
                    'document': d.document.url
                }]
        respuesta['data'] = ordenanzas
        print(respuesta)
        return JsonResponse(
            respuesta,
            status=200
        )
        # ordenanzas_serialized = serializers.serialize('json', ordenanzas)
        # result["ordenanzas"] = ordenanzas
        # data = json.dumps(result)
        # return JsonResponse(ordenanzas_serialized, safe=False)
        # return HttpResponse(respuesta, content_type='application/json')

    return render(request, 'ordenanzas/list_ordenanzas.html')
