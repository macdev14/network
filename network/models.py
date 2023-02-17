from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps

class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)
    following = models.ManyToManyField('self', blank=True) 

    def json(self):
        print('followers', self.following.all())
    
        return {
            'id':    self.pk,
            'email':    str(self.email),
            'followers': [self.get_followers()],
            'following':   [self.get_following()],
            'username': self.username

        }

    def get_followers(self):
        followers = list()
        for i in self.followers.all():
            followers.append( {
            'id':    self.pk,
            'email':    str(self.email),
            # 'followers': [i.json(n-1) for i in self.followers.all()],
            # 'following':   [i.json(n-1) for i in self.following.all()],
            'username': self.username

        })
        return followers

    def get_following(self):
        following = list()
        for i in self.following.all():
            following.append( {
            'id':    self.pk,
            'email':    str(self.email),
            # 'followers': [i.json(n-1) for i in self.followers.all()],
            # 'following':   [i.json(n-1) for i in self.following.all()],
            'username': self.username

        })
        return following
            
        

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='like_post')
    liked_date = models.DateTimeField(auto_now_add=True)

    def json(self):
        return {
            'id':    self.pk,
            'datetime':    str(self.datetime),
            'description': self.description,
            'title':   self.title,
            'user' : self.user.json()
        }




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name='post_like')
    # unlike = models.ForeignKey(Unlike, on_delete=models.CASCADE, related_name='post_unlike')
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.description

    def get_number_likes(self):
        l = apps.get_model('network','Like')
        return l.objects.filter(post=self.__class__).count()
    
    def get_number_unlikes(self):
        l = apps.get_model('network','Unlike')
        return l.objects.filter(post=self.__class__).count()

    def json(self, user_id=None):
        Unlike = apps.get_model('network','Unlike')
        like = apps.get_model('network','Like')
        data = {
            'id':    self.pk,
            'datetime':    str(self.datetime),
            'description': self.description,
            'title':   self.title,
            'user' :self.user.json(),
            
        }
        if user_id:
            data['liked'] = like.objects.filter(user__pk=user_id, post__pk=self.pk).exists()
            data['unliked'] = Unlike.objects.filter(user__pk=user_id, post__pk=self.pk).exists()
        

        if user_id == self.user.id:
            data['edit'] = True
        else: data['edit'] = False
        return data
    
    

class Unlike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='unlike_post')
    unliked_date = models.DateTimeField(auto_now_add=True)

    def json(self):
        return {
            'id': self.pk,
            'post': self.post.json(),
            'user': self.user.json(),
            'unliked_date': str(self.unliked_date),
        }
