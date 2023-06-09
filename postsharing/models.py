from django.db import models
from django.urls import reverse
from accounts.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='post', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_comment_count(self):
        return self.comments.count()
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])
    
class Comment(models.Model):
    content = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.user.username + ' likes ' + self.post.title

class Connection(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_creator_set")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendship_set")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return self.follower.username + ' follows ' + self.following.username
