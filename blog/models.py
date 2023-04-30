from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .managers import PostPublishedManager


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    body = models.TextField(verbose_name='Content')
    publish = models.DateTimeField(default=timezone.localtime)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=255)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='posts')


    objects = models.Manager()
    published = PostPublishedManager()


    class Meta:
        ordering = ('-publish', '-created')

    def __str__(self):
        return self.title


# Дописати модель Коментар(є автор, відноситься до посту),
class Comment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='Content')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    def __str__(self):
        return self.body


# Пост лайк/дизлайк(є автор, відноситься до посту),
class PostLikeDislike(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    LIKE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes_dislikes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes_dislikes')
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default=LIKE)

    def __str__(self):
        return f'{self.value} {self.post} by {self.author}'


# Коментар лайк/дизлайк (є автор, відноситься до коментаря),
class CommentLikeDislike(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    LIKE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes_dislikes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes_dislikes')
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default=LIKE)

    def __str__(self):
        return f'{self.value} {self.comment} by {self.author}'


# модель підписки на користувача два поля (хто підписався і на кого підписався).
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} subscribed to {self.subscribed_to}'
