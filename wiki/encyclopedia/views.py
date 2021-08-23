from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import markdown
import random

from . import util

class creationInput(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control ','rows':'20','placeholder':'#This is a heading,       [This is a Link](/wiki/ANYPAGE),        >Thats a quote',}))
    edit = forms.CharField(widget=forms.TextInput(attrs={'type':'hidden', 'value':'false'}))

def index(request):
    return render(request, "encyclopedia/start.html")
def home(request,*args):
    if not args:
        allEntries = util.list_entries()
    elif args[0] == "leer":
        return render(request, "encyclopedia/errors.html",{
            "title": "NoPageFound",
            "errorHead":"Page Not Found",
            "errorMessage":"does not exist",
            "thisOrAnother":"this"
            })
    else:
        allEntries = args
    descriptionList = {}
    for entry in allEntries:
        description = "";
        content = util.get_entry(entry)
        try: 
            for i in range(1,71):
                description=description+content[i]
                descriptionList[entry] = description
        except IndexError as error:
            descriptionList[entry] = description
               
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "descriptionsx":descriptionList,
        "allEntries":args
    })


def FindPage(request, name):
    if request.method == 'POST':
        title = request.POST.get("q")
        pageContent = util.get_entry(title)
        allEntries = util.list_entries()
        if pageContent == None:
            filteredEntries = []
            for entrie in allEntries:
                if title.lower() in entrie.lower():
                    filteredEntries.append(entrie)
            if len(filteredEntries) <= 0:
                    filteredEntries.append("leer")
            return home(request, *filteredEntries)
        else:
            pageContent = markdown.markdown(pageContent)
            return render(request, "encyclopedia/contentPage.html",{
            "title": title,
            "content":pageContent
            })
        
    else:
        title = name
        pageContent = util.get_entry(name)

        if pageContent == None:
            return render(request, "encyclopedia/errors.html",{
            "title": title,
            "errorHead":"Page Not Found",
            "errorMessage":"does not exist",
            "thisOrAnother":"this"
            })
        else:
            pageContent = markdown.markdown(pageContent)
            return render(request, "encyclopedia/contentPage.html",{
            "title": title,
            "content":pageContent
            })

def CreatePage(request):
    if request.method =='POST':
        form = creationInput(request.POST)
        if form.is_valid():
            title= form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title)== None or form.cleaned_data["edit"] == 'true':
                util.save_entry(title, content)
                return HttpResponseRedirect('/wiki/'+title)
            else:
                return render(request, "encyclopedia/errors.html",{
                "title":title,
                "errorHead":"Page Already Exists",
                "errorMessage": "already exists",
                "thisOrAnother":"another"
                })
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/creationPage.html", {
        "das":creationInput(),
        "title":"Create",
        "submitMessage":"Create"
        })

def RandomPage(request):
	allPages = util.list_entries()
	if len(allPages) > 0:
	    calculatedPage = random.choice(allPages)
	    return FindPage(request, calculatedPage)
	else:
	    return HttpResponseRedirect(reverse("index"))

def EditPage(request,name):
    content = util.get_entry(name)
    requestedPage = creationInput(initial={"title":name, "content":content})
    requestedPage.fields['title'].widget.attrs.update({'readonly':'readonly'})
    requestedPage.fields['edit'].widget.attrs.update({'value':'true'})
    return render(request, "encyclopedia/creationPage.html", {
    "edit":"true",
    "title":"Edit Page",
    "das": requestedPage,
    "submitMessage":"Save Changes"
    })

