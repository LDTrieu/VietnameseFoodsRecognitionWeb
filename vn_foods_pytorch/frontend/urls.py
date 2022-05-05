from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from frontend.views import (
    indexView,
    indexView2,
    indexView3,
    #searchResultView,
    postSearchResult,
    postPredictResult,
    #predictResultView,
    #checkID,
    #napImage,
    index2

)

urlpatterns = [
	#path('', views.index, name="index"),
    path('', indexView),
    #path('', postPredictResult),
    #path('post/ajax/result', postPredictResult, name = "post_result"),

    #path('api', index2,name="api"),
    #path('post/ajax/result', postSearchResult, name = "post_result"),
    #path('get/ajax/validate/nickname', checkID, name = "validate_id"),
    path('post/ajax/result', postPredictResult, name = "predict_result"),
    

    #path("cbv/", searchResultView.as_view(), name = "searchResult_cbv")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)