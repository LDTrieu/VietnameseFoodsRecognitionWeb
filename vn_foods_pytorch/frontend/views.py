import base64
import io
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from .forms import searchForm, predictForm
from .models import searchResult

from .forms import ImageUploadForm


def indexView(request):
    form = ImageUploadForm()
    searchResults = searchResult.objects.all()
    return render(request, "frontend/index.html",
     {"form": form, "searchResults": searchResults})

def indexView3(request):
    form = ImageUploadForm()
    searchResults = searchResult.objects.all()
    return render(request, "frontend/index.html",
     {"form": form, "searchResults": searchResults})

def indexView2(request):
    image_uri = None
    predicted_label = None
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.cleaned_data['image']
        image_bytes = image.file.read()
        encoded_img = base64.b64encode(image_bytes).decode('ascii')
        image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
        try:
             predicted_label = get_prediction(image_bytes)
             print(predicted_label)
        except RuntimeError as re:
            print(re)
    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_label': predicted_label,
    }

    return render(request, "frontend/index.html",context)

def postSearchResult(request):
    form = ImageUploadForm(request.POST, request.FILES)
    # request should be ajax and method should be POST.
    if   request.method == "POST":
        # get the form data
        form = searchForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)


def postPredictResult(request):
    image_uri = None
    predicted_label = None
    # request should be ajax and method should be POST.
        # get the form data
    form = ImageUploadForm(request.POST, request.FILES)
    #if   request.method == "POST":
        # save the data and after fetch the object in instance
    if form.is_valid():
        image = form.cleaned_data['image']
        image_bytes = image.file.read()
        encoded_img = base64.b64encode(image_bytes).decode('ascii')
        image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)
        try:
            predicted_label = get_prediction(image_bytes)
            print(predicted_label)
        except RuntimeError as re:
            print(re)
        
        #instance = form.save()
            # serialize in new friend object in json
        #ser_instance = serializers.serialize('json', [ instance, ])
        #print(ser_instance)
        context = {
                'encoded_img': encoded_img,
                'image_uri': image_uri,
                'predicted_label': predicted_label,
                }
            # send to client side.
        return JsonResponse(context, status=200)
    else:
        # some form errors occured.
        return JsonResponse({"error": form.errors}, status=400)
    #return JsonResponse()
    #return JsonResponse()
        #return JsonResponse(context, status=200)
        #return render(request, "frontend/index.html",context)
        

# # BONUS CBV
# def checkID(request):
#     # request should be ajax and method should be GET.
#     if  request.method == "GET":
#         # get the id from the client side.
#         id = request.GET.get("id", None)
#         # check for the nick name in the database.
#         if searchResult.objects.filter(id = id).exists():
#             # if id found return not valid new friend
#             return JsonResponse({"valid":False}, status = 200)
#         else:
#             # if id not found, then user can create a new friend.
#             return JsonResponse({"valid":True}, status = 200)

#     return JsonResponse({}, status = 400)


def searchResultView(View):
    form_class = searchForm
    template_name = "frontend/index.html"
    def get(self, *args, **kwargs):
        form = self.form_class()
        searchResults = searchResult.objects.all()
        return render(self.request, self.template_name, 
            { "searchResults": searchResults})
        
    def post(self, *args, **kwargs):
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            # get the form data
            form = self.form_class(self.request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)
        # some error occured
        return JsonResponse({"error": ""}, status=400)




import os
import json
from torchvision import models
from torchvision import transforms
from PIL import Image
from django.shortcuts import render
from django.conf import settings
from .forms import ImageUploadForm

json_path = os.path.join(settings.STATIC_ROOT, "imagenet_class_index.json")
imagenet_mapping = json.load(open(json_path))
model = models.densenet121(pretrained=True)
model.eval()

def transform_image(image_bytes):
    """
    Transform image into required DenseNet format: 224x224 with 3 RGB channels and normalized.
    Return the corresponding tensor.
    """
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    """For given image bytes, predict the label using the pretrained DenseNet"""
    tensor = transform_image(image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    class_name, human_label = imagenet_mapping[predicted_idx]
    return human_label


def index2(request):
    image_uri = None
    predicted_label = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_bytes = image.file.read()
            # convert and pass the image as base64 string to avoid storing it to DB or filesystem
            encoded_img = base64.b64encode(image_bytes).decode('ascii')
            image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)

            # get predicted label with previously implemented PyTorch function
            try:
                predicted_label = get_prediction(image_bytes)
                print(predicted_label)
            except RuntimeError as re:
                print(re)
    else:
        # in case of GET: simply show the empty form for uploading images
        form = ImageUploadForm()

    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_label': predicted_label,
    }
    return render(request,'frontend/index.html',context)

    