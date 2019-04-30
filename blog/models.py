from django.urls import reverse

from django.db import models
from django.utils import timezone

from .consts import *


class Section(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    disable = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'Section',
        null=True,
        blank=True,
        db_column='parent_id',
        on_delete=models.CASCADE,
        related_name='subsection'
    )

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('posts_sections', args=(self.pk,))
    
    def is_ordenanza(self):
        if self.pk == SECTION_ORDENANZA:
            return True
        return False


class Post(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='posts'
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return u'%s. %s' % (self.title, self.created_date)
    
    def get_add_comment_url(self):
        return reverse('add_comment', args=(self.pk,))

    def get_list_comment_url(self):
        return reverse('list_comment', args=(self.pk,))


class Comment(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_column='post_id',
        related_name='comentarios',
        verbose_name='Post',
    )

    class Meta:
        verbose_name = u'Cromentario'
        verbose_name_plural = u'Comentarios'
        permissions = (
            ("view_comment", u"Can view Comment"),
        )
    
    def __str__(self):
        return u'%s. %s' % (self.name, self.text)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    ordenanza = models.BooleanField(default=False)
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='post_id',
        related_name='documents',
        verbose_name='Post',
    )

    def __str__(self):
        return u'%s.' % (self.description)


class Image(models.Model):
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True  ,
        db_column='post_id',
        related_name='imagens',
        verbose_name='Post',
    )

    def __str__(self):
        return u'%s' % (self.image)


class BlacklistString(models.Model):
    string = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.string
    
    def save(self, *args, **kwargs):
        if self.string:
            self.string = self.string.strip().upper()
        super(BlacklistString, self).save(*args, **kwargs)


class Cargo(models.Model):
    descripcion = models.CharField(max_length=100, null=False, blank=False)


class Avatar(models.Model):
    apellido = models.CharField(max_length=60, null=False, blank=False)
    nombre = models.CharField(max_length=60, null=False, blank=False)
    cargo_id = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')

    class Meta:
        verbose_name = u'Avatar'
        verbose_name_plural = u'Avatares'
    
    def __str__(self):
        return self.cargo_id.descripcion
