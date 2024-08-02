from django.urls import path

from . import views

app_name = "wikiAppName"


urlpatterns = [
    path("", views.index, name="index"),
    path("showRandomWikiItemPage", views.showRandomWikiItemPage, name="showRandomWikiItemPage"),
    path("searchTheWiki", views.searchTheWiki, name="searchTheWiki"),
    path("addWiki", views.addWiki, name="addWiki"),
    path("editWiki", views.editWiki, name="editWiki"),
    path("editWiki/<str:wikiItem>", views.editWiki, name="editWiki"),
    path("<str:wikiItem>", views.showWikiItemPage, name="wikiItem"),
    path("wiki/<str:wikiItem>", views.showWikiItemPage, name="wikiItem")
]
