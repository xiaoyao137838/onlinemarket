from django import template
from postsharing.models import Connection, Like

register = template.Library()

@register.simple_tag
def is_followed_by_visitor(owner, visitor):
    followers = Connection.objects.filter(following=owner)
    return followers.filter(follower=visitor).exists()

@register.simple_tag
def has_user_liked_post(user, post):
    try:
        if Like.objects.filter(user=user, post=post).exists():
            return 'fa-heart'
        else:
            return 'fa-heart-o'
    except:
        return 'fa-heart-o'