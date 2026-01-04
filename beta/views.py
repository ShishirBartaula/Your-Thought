from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, userRegistrationForm #import from forms.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import Tweetserializer
from rest_framework import viewsets,permissions,parsers


def index(request):
    return render(request,"index.html")


# working on forms.py
def tweet_list(request):
    tweets =Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    #first it goes to else part
    #The user fills it out and hits "Submit".The view receives the data:
    #if form is valid then save the tweet.

    if (request.method=="POST"):
       #Browser: Sends a GET request.
       #It is NOT a POST, so it jumps to else .
       form= TweetForm(request.POST,request.FILES)
       if form.is_valid():
           tweet=form.save(commit=False) #tempory tweet .it donot have user name
           tweet.user=request.user  #extract user from currently logged in user.
           tweet.save()  #now save text+photo+user in database.
           '''
           Because TweetForm is a ModelForm ,
            you can just call form.save() in your view,
          and it automatically creates a database record. 
         You don't need to manually map tweet.text = request.POST['text'] .
           '''
           return redirect('tweet_list')
    else:#It sends the form to the HTML template.  The user fills it out and hits "Submit".
        form = TweetForm()
    return render(request,'tweet_form.html',{'form':form})
#render:this is a Django helper function that says: "Combine this HTML template with this
#  data and turn it into a final web page."

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)

    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        #Without instance=tweet : The user would see a blank form (like creating a new tweet).
        #With instance=tweet : The form is pre-filled with the existing tweet's data.
        if form.is_valid():
             tweet=form.save(commit=False)
             tweet.user=request.user
             tweet.save()
             return redirect('tweet_list')
        pass
    else:
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})


def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id, user= request.user)
    if(request.method=='POST'):
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet':tweet})


def register(request):
    if request.method=='POST':
        form=userRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:
        form=userRegistrationForm()

    return render(request,'registration/register.html',{'form':form})


# @api_view
class IsOwnerOrReadOnly(permissions.BasePermission):
    #This is a Custom Permission class. You need this to ensure that User A cannot edit User B's tweets .
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST','PUT','DELETE'):
            return True
        return obj.user == request.user
    
# @api_view  
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('id') #It gets all tweets and orders them by id so the newest ones are first
    serializer_class = Tweetserializer  #Tells the view which Serializer to use It uses Tweetserializer to convert tweets to JSON.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # - IsAuthenticatedOrReadOnly : You must be logged in to make changes. If you aren't logged in, you can only read.
# - IsOwnerOrReadOnly : (Our custom class from above) Even if you are logged in, you can only change your own tweets.
    parser_classes = [parsers.MultiPartParser, parsers.FormParser] #these parsers allow the API to handle image file uploads (Multipart forms).
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
