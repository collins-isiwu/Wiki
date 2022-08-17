from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util
import markdown2
import re
from random import choice


# Django forms for new page or entry
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control w-75'}))


# function to convert markdown to html
def convertToHTML(title):
    entry = util.get_entry(title)
    if entry:
        html = markdown2.markdown(entry)
        return html
    else:
        return None


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



# page that automatically renders a page - /wiki/{title}
def entry(request, title):
    # gets and stores the markdown content in content variable
    content = util.get_entry(title)

    # renders an error message if content doesn't exist
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page cannot be found"
        })

    # renders the page while converting the markdown to html
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convertToHTML(title)
        })



# search the entry 
def search(request):
    # saves the string from layout.html named q
    q = request.GET['q']
    content = util.get_entry(q)

    # if entry exists
    if content:
        return HttpResponseRedirect(reverse("entry", args=[q]))

    # if content doesn't exactly fit the list of the entries, use re to show the possible entry the user is looking for
    else:
        lstofEntries = util.list_entries()
        chances = []
        # re module in action
        string = re.compile("(?i)(" + q + ")")
        for lstofEntry in lstofEntries:
            # if users input matches entries, add them to chances
            if string.search(lstofEntry):
                chances.append(lstofEntry)

        # shows all the possible matches
        return render(request, "encyclopedia/search.html", {
            "string": q,
            "chances": chances
        })



def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]

            lstofEntry = util.get_entry(title)

            # check if the page exists via title, render an error if it does exist
            if (lstofEntry):
                return render(request, "encyclopedia/error.html", {
                "message": "This page already exists."
            })

            # else save the new entry and redirect user to the page created
            else:
                util.save_entry(title, description)
                return HttpResponseRedirect(reverse('entry', args=[title]))

    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm()
        })



class EditPage(forms.Form):
    edit = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '90'}))
    

def edit(request, title):
    # Prepopulate edit form
    form = EditPage(initial={'edit': util.get_entry(title)})

    # capture what the user edited and save in updatedEntry variable
    if request.method == 'POST':
        updatedEntry = EditPage(request.POST)

        # Check if form data is valid (server-side)
        if updatedEntry.is_valid():

            # Isolate the content from the 'cleaned' version of form data
            update = updatedEntry.cleaned_data["edit"]

            # save the new entry and redirect the user
            util.save_entry(title, update)
            return HttpResponseRedirect(reverse('entry', args=[title]))

    # else if the method is GET - LOAD a prepopulated page
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })


def random(request):

    lstofEntries = util.list_entries()

    # selects a title at random
    title = choice(lstofEntries)

    # redirect the user to the page
    return HttpResponseRedirect(reverse('entry', args=[title]))
