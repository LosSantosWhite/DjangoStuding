from django.contrib import admin
from .models import Post, Comment
from django.template.defaultfilters import truncatechars


class PostInLine(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "moderator_permission", "created", "updated", "status")
    list_filter = ("status",)
    search_fields = ("title", "body")
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("moderator_permission", "publish")
    actions = ["mark_as_published", "mark_as_draft"]
    inlines = [PostInLine]

    def mark_as_published(self, request, queryset):
        queryset.update(status="published")

    def mark_as_draft(self, request, queryset):
        queryset.update(status="draft")

    mark_as_published.short_description = 'Перевести в "Опубликовано"'
    mark_as_draft.short_description = 'Перевести в "Черновик"'

    def get_extra(self, request, obj=None, **kwargs):
        if obj.bar_set.count():
            return 0
        else:
            return 1


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'short_comment', 'active', 'email', 'created')
    list_display_links = ('short_comment',)
    list_filter = ('name',)

    actions = ["delete_comment"]

    def short_comment(self, obj):
        return truncatechars(obj.body, 15)

    def delete_comment(self, request, queryset):
        queryset.update(body='Комментарий удален администратором')

    delete_comment.short_description = 'Удалить комментарий'
