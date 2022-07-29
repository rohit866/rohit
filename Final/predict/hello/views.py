from __future__ import unicode_literals
from errno import ERANGE
from gettext import npgettext
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from matplotlib.style import context
import urllib3
import quandl
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection

from .forms import CreateUserForm
from .forms import TickerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from hello.models import Contact, Reply
from django.template import RequestContext
from .predict import get_meta_data, get_price_data



# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created  for ' + user)
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html/', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
             
    context = {}
    return render(request, 'login.html/', context)   

def logoutUser(request):
    logout(request)
    return redirect('login') 

def home(request):
    context = {}
    return render(request, 'index.html/', context)

def contact(request):
    context = {}
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        suggest = request.POST['suggest']
        message = request.POST['message']
        print(name, email, suggest, message)
        contact = Contact(name=name, email=email, suggest=suggest, message=message)
        contact.save()
    return render(request, 'contact.html/', context)

def news(request):
    context = {}
    if request.method=='POST':
        name = request.POST['name']
        message = request.POST['message']
        reply = Reply(name=name, message=message)
        reply.save()
    return render(request, 'news.html/', context)

def prediction(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            predict = request.POST['predict']
            return HttpResponseRedirect(predict)
    else:
        form = TickerForm()
    return render(request, 'prediction.html', {'form': form})


def search(request, tid):
    context = {}
    context['predict'] = tid
    context['meta'] = get_meta_data(tid)
    context['price'] = get_price_data(tid)
    return render(request, 'search.html/', context)


def predicts(request):
    # Quandl API key. Create your own key via registering at quandl.com
    quandl.ApiConfig.api_key = "RHVBxuQQR_xxy8SPBDGV"
    # Getting input from Templates for ticker_value and number_of_days
    ticker_value = request.POST.get('ticker')
    number_of_days = request.POST.get('days')
    number_of_days = int(number_of_days)
    # Fetching ticker values from Quandl API 
    df = quandl.get("WIKI/"+ticker_value+"")
    df = df[['Adj. Close']]
    forecast_out = int(number_of_days)
    df['Prediction'] = df[['Adj. Close']].shift(-forecast_out)
    # Splitting data for Test and Train
    X = np.array(df.drop(['Prediction'],1))
    X = preprocessing.scale(X)
    X_forecast = X[-forecast_out:]
    X = X[:-forecast_out]
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.2)
    # Applying Linear Regression
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    # Prediction Score
    confidence = clf.score(X_test, y_test)
    # Predicting for 'n' days stock data
    forecast_prediction = clf.predict(X_forecast)
    forecast = forecast_prediction.tolist()
    return render(request,'prediction.html',{'confidence' : confidence,'forecast': forecast,'ticker_value':ticker_value,'number_of_days':number_of_days})

