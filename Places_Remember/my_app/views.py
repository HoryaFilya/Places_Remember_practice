from django.shortcuts import render
from .forms import MemoryForm
from social_django.models import UserSocialAuth
import requests
from django.http import HttpResponseRedirect
from .models import Memory
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def login(request):
    return render(request, 'my_app/my_app.html')


def vk_auth_callback(request):
    user_social_auth_1 = UserSocialAuth.objects.get(user=request.user, provider='vk-oauth2')
    user_social_auth_2 = UserSocialAuth.objects.get(user=request.user, provider='google-oauth2')
    if request.user.is_authenticated and user_social_auth_2:
        access_token = user_social_auth_2.extra_data['access_token']
        api_url = f'https://www.googleapis.com/userinfo/v2/me?alt=json&access_token={access_token}'
        response = requests.get(api_url)
        data = response.json()
        first_name = data['name']
        photo_url = data['picture']
        download_photo(photo_url)
        info = Memory.objects.all()
        data_new = {
            'data_new': first_name,
            'info': info
        }
        return render(request, 'my_app/data_new.html', context=data_new)
    elif request.user.is_authenticated and user_social_auth_1:
        access_token = user_social_auth_1.extra_data['access_token']
        vk_user_id = user_social_auth_1.uid
        api_url = f'https://api.vk.com/method/users.get?user_ids={vk_user_id}&fields=last_name,photo_200&access_token={access_token}&v=5.131'
        response = requests.get(api_url)
        data = response.json()
        first_name = data['response'][0]['first_name']
        photo_url = data['response'][0]['photo_200']
        download_photo(photo_url)
        info = Memory.objects.all()
        data_new = {
            'data_new': first_name,
            'info': info
        }
        return render(request, 'my_app/data_new.html', context=data_new)
    return render(request, 'my_app/not_login.html')


def download_photo(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(BASE_DIR/'static/images/profile_photo.jpg', 'wb') as file:
            file.write(response.content)


def google(request):
    return render(request, 'my_app/google.html')


def vk(request):
    return render(request, 'my_app/vk.html')


def addmemory(request):
    form = MemoryForm(request.POST or None)
    data = {
        'form': form,
    }
    if request.method == 'POST' and form.is_valid():
        info = form.cleaned_data
        new_form = form.save()
        return HttpResponseRedirect('http://127.0.0.1:8000/login/info/')
    return render(request, 'my_app/addmemory.html', context=data)