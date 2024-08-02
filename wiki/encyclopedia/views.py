from django.shortcuts import render
from django.urls import reverse
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile, File

import pdb #debugger
import re #regular expressions
import markdown2 #md file to html converter
import random
import re

matchGroup = None

class NewSearchForm(forms.Form):
    searchForm = forms.CharField(label="Search the Wiki")

class NewWikiFormTitle(forms.Form):
    wikiTitle = forms.CharField(label="Provide wiki's title:", widget=forms.TextInput(attrs={'name':'titleBox'}))

class NewWikiFormBody(forms.Form):
    wikiBody = forms.CharField(label="Provide wiki's body:", widget=forms.Textarea(attrs={'name':'content','style':'width: 90%; height: 20vh; resize: none; margin-top: 1px;'}))

class EditWikiFormBody(forms.Form):
    #def setWikiTitle(self, wikiTitle):
    #    self.wikiTitle = wikiTitle
    #def setWikiBody(self, wikiTitle):
    #    self.edWikiBody = util.get_entry(wikiTitle)
    edWikiBody = forms.CharField(label="Provide wiki's body:", widget=forms.Textarea(attrs={'name':'content','style':'width: 90%; height: 20vh; resize: none; margin-top: 1px;'}), initial=util.get_entry('CSS'))


def searchTheWiki(request):
    if request.method == "POST":
        #if file is found for search, redirect to its existing wiki page
        formData = request.POST.dict()
        searchTerm = formData.get("q")
        wikiEntryBody = util.get_entry(searchTerm)

        if wikiEntryBody != None: #if there is a wiki entry body, then show it.
            return render(request, "encyclopedia/wiki-item-page.html", {
                "wikiPageTitle": searchTerm,
                "wikiItem": markdown2.markdown(util.get_entry(searchTerm)) #need to add a wikipage footer?
            }
        )

        #check for substrings if no exact match
        if wikiEntryBody == None:#proceed with check of partial match
            entriesToSearch = util.list_entries()
            partialEntriesFound = [x for x in entriesToSearch if re.search(searchTerm, x)]
            #breakpoint()

            if partialEntriesFound != None:
                return render(request, "encyclopedia/index.html", { #generate list of partial matches
                    "entries": partialEntriesFound
                })
            else:#no partial matches
                return render(request, "encyclopedia/not-found-page.html")
        
    else:#not a POST
        return render(request, "encyclopedia/not-found-page.html")


def index(request):
    #if "currentSessionWiki" not in request.session:
    #    request.session["currentSessionWiki"] = []    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showRandomWikiItemPage(request):
    wikiEntries = util.list_entries()

    if len(wikiEntries) > 0:
        randomWikiEntry = random.choice(wikiEntries)
        return render(request, "encyclopedia/wiki-item-page.html", {
            "wikiPageTitle": randomWikiEntry,
            "wikiItem": markdown2.markdown(util.get_entry(randomWikiEntry))        
        })
    else:
        return render(request, "encyclopedia/not-found-page.html")

    

def showWikiItemPage(request, wikiItem):
    #breakpoint()
    checkIfExists = util.get_entry(wikiItem)

    if checkIfExists == None:
        return render(request, "encyclopedia/not-found-page.html")
    
    else:
        return render(request, "encyclopedia/wiki-item-page.html", {
            "wikiPageTitle": wikiItem,
            "wikiItem": markdown2.markdown(util.get_entry(wikiItem))
        }
    )

def addWiki(request):
    if request.method == "POST":
        #if file is found for search, redirect to its existing wiki page
        formData = request.POST.dict()
        uiTitle = formData.get("wikiTitle")
        wikiEntryBody = util.get_entry(uiTitle)

        if wikiEntryBody != None: #if there is a wiki entry body, then don't add it to wiki.
            return render(request, "encyclopedia/page-already-exists.html")
        else: 
            with open("entries/" + uiTitle + ".md", "w") as f:
                myfile = File(f)
                myfile.write(formData.get("wikiBody"))
                myfile.close()
                return render(request, "encyclopedia/wiki-item-page.html", {
                    "wikiPageTitle": uiTitle,
                    "wikiItem": markdown2.markdown(util.get_entry(uiTitle))        
                })           
    return render(request, "encyclopedia/add.html", {
        "formTitle": NewWikiFormTitle(),
        "formBody": NewWikiFormBody()
    })

def editWiki(request, wikiItem):

    currentWikiTitle = request.path
    foundMatch = re.search("[^\/]+$", currentWikiTitle)
    matchGroup = foundMatch.group()    

    if request.method == "POST":
        #update existing wiki entry and redirect to its modified wiki page
        formData = request.POST.dict()
        #breakpoint()

        with open("entries/" + matchGroup + ".md", "w") as f:
            myfile = File(f)
            myfile.write(formData.get("myTextArea"))
            myfile.close()
            return render(request, "encyclopedia/wiki-item-page.html", {
                "wikiPageTitle": matchGroup,
                "wikiItem": markdown2.markdown(util.get_entry(matchGroup))        
            })      


    #request.session["currentSessionWiki"] = matchGroup
    #if request.method == "POST":

    #objToPass = EditWikiFormBody()
    #objToPass.setWikiTitle(wikiItem)
    #objToPass.setWikiBody(wikiItem)
      
    return render(request, "encyclopedia/edit.html", {        
        #"formBody": EditWikiFormBody(),
        "editWikiPageTitle": matchGroup,
        "taBody": util.get_entry(matchGroup)
    })