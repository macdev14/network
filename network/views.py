from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from network.forms import PostForm
from network.permissions import PostPermission
from .models import Like, Post, Unlike, User
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.db.models import Q
from django.core import serializers
@register.filter
def get_range(value):
    if value:
        return range(1, value)
    return None

@register.filter
def likes(object, user):
    if Like.objects.filter(post=object,user=user).exists():
        return True
    return False


class CSRFExemptMixin(object):
   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
       return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


class ListPosts(ListView):
    model = Post
    paginate_by = 2
    template_name = 'network/post/list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(description__icontains=query) | Q(title__icontains=query)  | Q(user__username__icontains=query) )
        return super().get_queryset()

class ListFollowingPosts(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'network/post/list-post.html'

    def get_queryset(self):
        post = []
       
        for user in self.request.user.following.all():
            post.append(Post.objects.get(user=user))
        return post



class CreatePost(CreateView):
    model = Post
    template_name='network/post/create.html'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_success_url(self):
        
        return reverse('index')


class UpdatePost(PostPermission, UpdateView):
    model = Post
    template_name='network/post/update.html'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def get_success_url(self):
        
        return reverse('index')

class DeletePost(PostPermission, DeleteView):
    model = Post
    template_name='network/post/delete.html'

    
    
    def get_success_url(self):
        
        return reverse('index')

class AddPostAPI(CSRFExemptMixin, View):
    def post(self, request):
        print('called')
        data = json.loads(request.body)
        Post.objects.create(user=request.user, title=data.get('title'),description=data.get('description'))
        return JsonResponse({"message": "Post created successfully."}, status=201)
    def get(self, request):
        
        return JsonResponse({"error": "POST request required."}, status=400)
    

class UpdatePostAPI(CSRFExemptMixin, View):


    def get(self, request, pk):
        print(pk)
        post = Post.objects.filter(pk=pk).exists()
        print(post)
        if not pk or not post: 
            return JsonResponse({"error": "Post not found"}, status=400)
        data = Post.objects.get(pk=pk).json()
        return HttpResponse(json.dumps(data), content_type="application/json")
        

    def put(self, request, pk):
        
        print('PRIMARY KEY', pk)
        if not pk : 
            return JsonResponse({"error": "Post not found"}, status=400)
        data_pk = pk
        data = json.loads(request.body)
        po = Post.objects.filter(pk=data_pk).exists()
        if po:
            post_object = Post.objects.get(pk=data_pk)
            same_user = post_object.user == request.user
            if same_user:
                    # po.description = data.get('description')
                if data.get('like'):
                    ul = Unlike.objects.filter(user=request.user, post=post_object)
                    ul.delete()
                    Like.objects.create(user=request.user, post=post_object)
                    
                    return JsonResponse({"message": "Post liked successfully."}, status=201)
                elif data.get('unlike'):
                    l = Like.objects.filter(user=request.user, post=post_object)
                    l.delete()
                    ul = Unlike.objects.create(user=request.user, post=post_object)
                    return JsonResponse({"message": "Post unliked successfully."}, status=201)
                elif data.get('title') and data.get('description'):
                    post_object.title = data.get('title')
                    post_object.description = data.get('description')
                    post_object.save()
                    return JsonResponse({"message": "Post updated successfully."}, status=201)

            else: 
                return JsonResponse({"error": "Different User"}, status=400)
        else:
            return JsonResponse({"error": "Post not found"}, status=400)
        return JsonResponse({"error": "Post not found"}, status=201)
        
            
        

        
            

    
class ListFollowingProfileAPI(CSRFExemptMixin, LoginRequiredMixin, View):
    

    def get(self, request , pk):
        post = []
        user = User.objects.get(pk=pk)
        # for user in self.request.user.following.all():
        post = Post.objects.filter(user__pk=pk)
        
        data = [ i.json(request.user.id) for i in post]
        
        if user in self.request.user.following.all():
            data.insert(0, {'following': True})
        else:
            data.insert(0, {'following': False})
        print(data)
        return JsonResponse({'data':data})

    
class ListFollowingPostsAPI(CSRFExemptMixin,LoginRequiredMixin, View):
    

    def get(self, request , pk=None):
        post = []
        
        for user in self.request.user.following.all():
            post.append(Post.objects.get(user=user))
        return HttpResponse(json.dumps(post), content_type="application/json")

class ListPostsAPI(View):
    

    def get(self, request):
        if request.user.is_authenticated:
            data = [i.json(request.user.id) for i in Post.objects.all()]
        else:
            data = [i.json() for i in Post.objects.all()]
        print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")

        
class DeletePostAPI(CSRFExemptMixin, View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            exists = Post.objects.filter(pk=data.get('id')).exists()
            
            if exists:
                post = Post.objects.get(pk=data.get('id'))
                same_user = post.user == request.user
                if same_user:
                    post.delete()
                    return JsonResponse({"message": "Post deleted successfully."}, status=201)
                else: return JsonResponse({"error": "Post from different user."}, status=400)
            return JsonResponse({"error": "POST not found."}, status=400)
        else:
            return  JsonResponse({"error": "User not authenticated."}, status=403)
                
    
        
        
    def get(self, request):
        
        return JsonResponse({"error": "POST request required."}, status=400)
        
        
class FollowUserAPI(CSRFExemptMixin, LoginRequiredMixin, View):

    def post(self, request):
        data = json.loads(request.body)
        if User.objects.filter(pk=data.get('id')).exists(): 
            user_object = User.objects.get(pk=data.get('id'))
            if user_object in self.request.user.following.all():
                request.user.following.remove(user_object)
                return JsonResponse({"message": "User unfollowed successfully."}, status=201)
            request.user.following.add(user_object)
            user_object.followers.add(request.user)
            user_object.save()
            request.user.save()
            return JsonResponse({"message": "User followed successfully."}, status=201)
        return JsonResponse({"error": "User not found"}, status=400)