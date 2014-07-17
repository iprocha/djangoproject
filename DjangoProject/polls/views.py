# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from polls.models import Question

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from polls.models import Document
from polls.forms import DocumentForm
import sys
import codecs
import MySQLdb
import datetime

def index(request):
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = request.FILES['docfile']
            docname = docfile.name;
            docname = docname.split("/")[-1]
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.docfile.name = docname
            print(newdoc.docfile.name)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('polls.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    for document in documents:
        docname = document.docfile.name
        document.docfile.name = docname.split("/")[-1]

    # Render list page with the documents and the form
    return render_to_response(
        'polls/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
def deleteDocument(request, document_id):
    document = Document.objects.get(id=document_id)
    if(document):
        document.delete()
    form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    for document in documents:
        docname = document.docfile.name
        document.docfile.name = docname.split("/")[-1]
    return render_to_response(
        'polls/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
 
def indexDocument(request, document_id):
    horaInicio = datetime.datetime.now()
    document = Document.objects.get(id=document_id)
    document_path = document.docfile.path
    fp_pnae_html = codecs.open(document_path,encoding="utf8")
    pnae = fp_pnae_html.read()
    pnae = pnae.replace(">","> ")
    pnae = pnae.replace("<"," <")
    pnae = pnae.split()
    fp_pnae_html.close()
    
    
     
    

    
    #Recebe uma lista de palavras e retorna um cojunto dos graus de todos as palavras contidas na lista
    def words_order_set(lista_palavras):
        lista_graus = [len(lista_palavras[x][0].split(" ")) for x in range(len(lista_palavras))]
        lista_graus_sorted = sorted(lista_graus, reverse=True)
        conjunto = set(lista_graus_sorted)
        lista_graus = [conjunto.pop() for x in range(len(conjunto))]
        return lista_graus
    
    #Conexao com o banco de dados
    db = MySQLdb.connect(host="127.0.0.1", 
                         port=3306,
                         user="root", 
                          passwd="81726354", 
                          db="processer", 
                          ) 
    
    # you must create a Cursor object. It will let
    #  you execute all the query you need
    cur = db.cursor() 
    print("passou aqui")
    # Use all the SQL you LikeCond
    
    
    db.set_character_set('utf8') 
    cur.execute('SET NAMES utf8;') 
    cur.execute('SET character_set_connection=utf8;')
    
    
    sql = "Select nome from termosteste where nome LIKE '%s\%'"
    
    punctuation = "!\()*+,-./:;=?@[\\]_`{|}"
    
    w = 0
    while w < (len(pnae)):
        encontrouComposto = False
        #Se tiver alguma tag html passa pra proxima palavra
        if "<" in pnae[w] or ">" in pnae[w]:
            w = w+1
            continue
        #Somente para termo simples. Se o termo simples for encontrado na lista de stopwords entao ele eh desconsiderado
        #e o algoritmo passa para a proxima palavra.
        isStopword = False
        cur.execute(r'Select nome from stopwords where nome LIKE %s', pnae[w].lower().encode("utf-8") )
        isStopword = cur.fetchall()
        if(isStopword):
            #Incrementa 1 no contador dos termos do pnae, passando para a proxima palavra.
            #Nao executa o algoritmo para esse termo
            w = w+1
            continue
        
        #Caso contrario procura termo simples e seus derivados no dicionario de termos.
        termo_simples = pnae[w].encode("utf-8").lower().strip(punctuation)+"%"
        cur.execute(r'Select nome from termoscamara where nome LIKE %s',termo_simples)
        data = cur.fetchall()
    
            #print(data)
        #Se encontra algum termo simples, ou seja, data conter alguma informacao, entao entre no if.
        if(data):
            #Laco que percorre uma lista de graus de cada expressao que contem o termo simples encontrado.
            #A lista estah em ordem decrescente
            for x in reversed(words_order_set(data)):
                #Se o indice corrente eh menor que o tamanho da lista entao checar palavra,
                #caso contrario, dar um continue e pular para o proximo grau
                if((w+x) < len(pnae)):
                    termo_composto = " ".join(pnae[w:(w+x)]).strip(punctuation).encode("utf-8").lower()
                else:continue
                
                cur.execute(r'Select nome, significado from termoscamara where nome LIKE %s',termo_composto)
                composto_encontrado = cur.fetchall()
                
                #Se um termo composto eh encontrado
                if(composto_encontrado):
                    
                    significado = composto_encontrado[0][1].decode("utf-8")
                    if(x == 1):
                        palavra_indexada = '<a title="'+significado+'"><b><Font color="blue">'+pnae[w]+'</font></b></a>'
                        pnae[w] = palavra_indexada
                    elif(x > 1):
                        composto_indexado_inicio = '<a title="'+significado+'"><b><Font color="red">'+pnae[w]
                        pnae[w] =  composto_indexado_inicio
                        composto_indexado_final = pnae[w+x-1]+'</font></b></a>'
                        pnae[w+x-1] = composto_indexado_final
                    print("Composto Encontrado:")
                    print(composto_encontrado) 
                    print(" finalComposto")
                    #Jah que o termo composto foi encontrado, desconsidera-se as palavras do termo e pula-se as devidas posicoes.
                    w += x
                    encontrouComposto = True
                    break
        #Se um termo composto foi encontrado pula para o proximo termo, de acordo com o grau do termo encontrado
        #Caso contrario passa para o proximo termo
        if(encontrouComposto):
            continue
        else:
            print
            w = w + 1
                  
                    
    horaFim = datetime.datetime.now()                
    print("acabou")
    cur.close()
    db.close()
    
    # exit()
    
    #saida de dados
    root_path = "C:/IGOR_TRABALHO/AEB/PESQUISA_PLN"
    pnae = " ".encode("utf-8").join(pnae)
    pnae_utf8 = pnae.encode("utf-8")
    fp_saida = open(root_path + r"/TESTES/Teste_Expressoes16.html","w")
    fp_saida.write(pnae_utf8.__str__())
    fp_saida.close()
    print("arquivo criado com sucesso!")
    
    response = HttpResponse(pnae_utf8,content_type='text/html')
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="indexedFile.HTML"' 
    print(response)   
    
    return response
        
        