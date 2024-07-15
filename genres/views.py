import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt # modulo se segurança 
from genres.models import Genre

@csrf_exempt   #modulo de segurança obrigatorio ter !
def genre_create_list_view(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        data = [{'id': genre.id, 'name': genre.name} for genre in genres]
        return JsonResponse(data, safe=False) #è esperado safe=False
    elif request.method == 'POST':
        # loads -> pega formato Json e torna em lista para manioulação em Python
        data = json.loads(request.body.decode('utf-8')) #pegar os dados vindo body e decodificando formato UTF-8 
        new_genre = Genre(name=data['name'])
        new_genre.save() 
        return JsonResponse(
            {'id': new_genre.id, 'name': new_genre.name},  #ta retornando para body(usuario)
            status=201 # status 201 -> Criado  com Sucesso!
        )  # obs no POSTMAN POST -> Body -> ram -> JSON -> Escrevar daos em formato Json


@csrf_exempt
def genre_detail_view(request, pk):
    #get_object_or_404 -> page ojeto se existir segue senão da erro 404(Nao encontrado) padrão HTTP
    genre = get_object_or_404(Genre, pk=pk)
    if request.method == 'GET':
        data = {'id': genre.id, 'name': genre.name}
        return JsonResponse(data)
    elif request.method == 'PUT':  # PUT = UPDATE 
        data = json.loads(request.body.decode('utf-8'))
        genre.name = data['name']
        genre.save()
        return JsonResponse(
            {'id': genre.id, 'name': genre.name}
        ) 
    elif request.method == 'DELETE':
        genre.delete()
        return JsonResponse(
            {'message': 'Gerero excluído com sucesso.'},
            status=204,      #status 204 padrão delete
        )      