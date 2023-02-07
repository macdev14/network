from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class PostPermission(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        print('CALLED')
        print(post.user)
        
        print('user', self.request.user)
        return post.user == self.request.user

    def permission_denied_message(self):
        messages.error(self.request, 'Restricted')
        print('denied')
        return redirect('index')