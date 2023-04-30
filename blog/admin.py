from django.contrib import admin

from .models import Category, Post, Comment, Subscription, PostLikeDislike, CommentLikeDislike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    list_filter = ('status', 'created', 'author')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    raw_id_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created')
    search_fields = ('body',)
    list_filter = ('created',)
    raw_id_fields = ('author', 'post')

@admin.register(PostLikeDislike)
class PostLikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'value')
    list_filter = ('value',)
    search_fields = ('post__title', 'user__username')
    raw_id_fields = ('post', 'author')
#
@admin.register(CommentLikeDislike)
class CommentLikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'value')
    raw_id_fields = ('author', 'comment')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to')
    raw_id_fields = ('subscriber', 'subscribed_to')

