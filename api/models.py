import datetime
import uuid

from django.db import models
from rest_framework_jwt.serializers import User
from django.conf import settings
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.utils.text import slugify
import string
import random

KATEGORILER = (
    ('Gündem','Gündem'),
    ('Liste', 'Liste'),
    ('Test','Test'),
    ('Goygoy','Goygoy'),
    ('Dizi ve Film','Dizi ve Film'),
    ('Kültür ve Sanat','Kültür ve Sanat'),
    ('Moda','Moda'),
    ('Spor','Spor'),
    ('Teknoloji ve Bilim','Teknoloji ve Bilim'),
    ('Astroloji', 'Astroloji'),
    ('Yemek', 'Yemek'),
    ('Oyun', 'Oyun'),
)

def nameFile(instance, filename):
    return '/'.join(['thumbnails', str(instance.id), filename])


def nameFile2(instance, filename):
    return '/'.join(['userprofiles', str(instance.user), filename])


def nameFile3(instance, filename):
    return '/'.join(['gorsels', str(instance.olusturan), filename])


def nameFile4(instance, filename):
    return '/'.join(['kapak', str(instance.user), filename])


def nameFile5(instance, filename):
    return '/'.join(['grup', str(instance.name), filename])


def nameFile6(instance, filename):
    return '/'.join(['grupicerigi', str(instance.icerik), filename])


def nameFile7(instance, filename):
    return '/'.join(['sorugorseli', filename])


def nameFile8(instance, filename):
    return '/'.join(['sonucgorseli', filename])


def nameFile9(instance, filename):
    return '/'.join([filename])


def nameFile10(instance, filename):
    return '/'.join(['question-answ', filename])


def nameFile11(instance, filename):
    return '/'.join(['question', filename])


def nameFile12(instance, filename):
    return '/'.join(['poll-answer', filename])


def nameFile13(instance, filename):
    return '/'.join(['poll-question', filename])


class PersonalityResult(models.Model):
    sonuc = models.TextField(max_length=100)
    descr = models.TextField(max_length=800, default='', blank=True, null=True)
    img = models.ImageField(upload_to=nameFile8, blank=True, null=True)


class PersonalityAnswer(models.Model):
    body = models.TextField(max_length=100)
    img = models.ImageField(upload_to=nameFile9, blank=True)
    result = models.ForeignKey(PersonalityResult, related_name='personalityresults', on_delete=models.CASCADE, null=True, blank=True)


class PersonalityQuestion(models.Model):
    title = models.TextField(max_length=100, default='', null=False, blank=False)
    body = models.TextField(max_length=100, default='', null=True, blank=True)
    img = models.ImageField(upload_to=nameFile7, blank=True, null=True)
    answer = models.ManyToManyField(PersonalityAnswer, related_name='personality_answer', null=True, blank=True)
    olusturan = models.TextField(max_length=18, default='', null=False, blank=False)


class QuizAnswers(models.Model):
    body = models.TextField(max_length=100)
    img = models.ImageField(upload_to=nameFile10, blank=True, null=True)
    dogrumu = models.TextField(max_length=100, default='false', null=False, blank=False)


class Quiz(models.Model):
    title = models.TextField(max_length=100, default='', null=False, blank=False)
    body = models.TextField(max_length=100, default='', null=True, blank=True)
    img = models.ImageField(upload_to=nameFile11, blank=True, null=True)
    answer = models.ManyToManyField(QuizAnswers, related_name='quiz_answer', null=True, blank=True)
    olusturan = models.TextField(max_length=18, default='', null=False, blank=False)


class PollAnswer(models.Model):
    body = models.TextField(max_length=100)
    img = models.ImageField(upload_to=nameFile12, blank=True, null=True)
    katilanlarsecret = models.ManyToManyField(User, related_name='katilanlargizli', null=True, blank=True)
    katilanlar = models.ManyToManyField(User, related_name='katilanlaracik', null=True, blank=True)


class PollQuestion(models.Model):
    question = models.TextField(max_length=100, default='', null=False, blank=False)
    body = models.TextField(max_length=100, default='', null=False, blank=False)
    img = models.ImageField(upload_to=nameFile13, blank=True, null=True)
    answer = models.ManyToManyField(PollAnswer, related_name='poll_answer', null=True, blank=True)
    olusturan = models.TextField(max_length=18, default='', null=False, blank=False)


def create_slug(title):  # new
    slug = slugify(title)
    qs = Content.objects.filter(kisalink=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" % (slug, qs.first().id)
    return slug


class Content(models.Model):
    title = models.CharField(max_length=175)
    kisalink = models.SlugField(null=True, blank=True, unique=True) # new
    ozet = models.TextField(max_length=360)
    olusturan = models.TextField(max_length=18)
    olusturanid = models.TextField(max_length=18)
    thumbnail = models.ImageField(upload_to=nameFile, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sliderde = models.BooleanField(default=False)
    yayinda = models.BooleanField(default=False)
    liste = models.TextField(max_length=10000, blank=True, null=True)
    listeicerik = models.TextField(max_length=10000, blank=True, null=True)
    listegorsel = models.TextField(max_length=10000, blank=True, null=True)
    kategori = models.TextField(max_length=900, choices=KATEGORILER, default='Gundem', null=False)
    begenenler = models.ManyToManyField(User, related_name='content_liked', null=True, blank=True)
    vucut = HTMLField(null=False)
    okuyacaklar = models.ManyToManyField(User, related_name='content_okuyacak', null=True, blank=True)
    goruntulenme = models.IntegerField(default=0)
    hashtagler = models.TextField(max_length=900, null=True, blank=True)
    test = models.ManyToManyField(PersonalityQuestion, related_name='personality_quest', null=True, blank=True)
    quiz = models.ManyToManyField(Quiz, related_name='content_quiz', null=True, blank=True)
    poll = models.ManyToManyField(PollQuestion, related_name='content_quiz', null=True, blank=True)
    endiseli = models.ManyToManyField(User, related_name='emoji_endise', null=True, blank=True)
    komik = models.ManyToManyField(User, related_name='emoji_komik', null=True, blank=True)
    sinirli = models.ManyToManyField(User, related_name='emoji_sinirli', null=True, blank=True)
    alkis = models.ManyToManyField(User, related_name='emoji_alkis', null=True, blank=True)
    saskin = models.ManyToManyField(User, related_name='emoji_saskin', null=True, blank=True)
    uzgun = models.ManyToManyField(User, related_name='emoji_uzgun', null=True, blank=True)
    igrenc = models.ManyToManyField(User, related_name='emoji_igrenc', null=True, blank=True)
    sevdim = models.ManyToManyField(User, related_name='emoji_sevdim', null=True, blank=True)


    def save(self, *args, **kwargs):

        if not self.kisalink:
            self.kisalink = create_slug(self.title)

        try:
            points = settings.POINTS_SETTINGS['CREATE_ARTICLE']
            dailypoints = settings.POINTS_SETTINGS['CREATE_ARTICLE']
            Profile.objects.get(user=self.olusturanid).modify_points(points)
            Profile.objects.get(user=self.olusturanid).modify_daily_points(dailypoints)
            usser = Profile.objects.get(user=self.olusturanid)
            usser.rozetler.add(1)

        except KeyError:
            points = 0
        return super().save(*args, **kwargs)

class ContentComment(models.Model):
    post = models.ForeignKey(Content, related_name='contentcomment', on_delete=models.CASCADE, null=True, blank=True)
    yazan = models.TextField(max_length=18)
    yazanid = models.TextField(max_length=18)
    body = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    yukari = models.ManyToManyField(User, related_name='contentcomment_up', null=True, blank=True)
    asagi = models.ManyToManyField(User, related_name='contentcomment_down', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                points = settings.POINTS_SETTINGS['CREATE_COMMENT']
                dailypoints = settings.POINTS_SETTINGS['CREATE_COMMENT']
            except KeyError:
                points = 0

            Profile.objects.get(user=self.yazanid).modify_points(points)
            Profile.objects.get(user=self.yazanid).modify_daily_points(dailypoints)
            usser = Profile.objects.get(user=self.yazanid)
            usser.rozetler.add(2)

        super(ContentComment, self).save(*args, **kwargs)

class FollowerRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='user_follower')
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)


class Group(models.Model):
    image_url = models.ImageField(upload_to=nameFile5, blank=True, null=True, default='/grup/default.jpg')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, max_length=80, default='')
    bilgilendirme = models.TextField(blank=True, max_length=800, default='')
    gizligrup = models.TextField(blank=False, default='0')
    yoneticiler = models.ManyToManyField(User, related_name='grup_yoneticileri', null=True, blank=True)
    uyeler = models.ManyToManyField(User, related_name='grup_uyeleri', null=True, blank=True)
    uyelerasil = models.ManyToManyField(User, related_name='grup_uyelerasil', null=True, blank=True)
    olusturulma = models.DateTimeField(auto_now_add=True)
    puan = models.PositiveIntegerField(default=0, blank=True, null=True)

    def modify_points(self, added_points):
        self.puan += added_points
        self.save()


class GrupIcerikleri(models.Model):
    grup = models.ForeignKey(Group, related_name='icerikgrup', on_delete=models.CASCADE, null=True, blank=True)
    icerik = models.TextField(max_length=180)
    yazan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=nameFile6, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    begenenler = models.ManyToManyField(User, related_name='icerikgrup_begenenler', null=True, blank=True)
    puan = models.PositiveIntegerField(default=0, blank=True, null=True)

    def modify_points(self, added_points):
        self.puan += added_points
        self.grup.puan += added_points
        self.save()

    def save(self, *args, **kwargs):
        try:
            points = settings.POINTS_SETTINGS['GROUP_CONTENT']
        except KeyError:
            points = 0
        Group.objects.get(pk=self.grup.id).modify_points(points)
        super(GrupIcerikleri, self).save(*args, **kwargs)


class GrupIcerikleriComment(models.Model):
    blogpost = models.ForeignKey(GrupIcerikleri, related_name='grupiceriklericomments', on_delete=models.CASCADE, null=True, blank=True)
    yazan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    yukari = models.ManyToManyField(User, related_name='gcontentcomment_up', null=True, blank=True)
    asagi = models.ManyToManyField(User, related_name='gcontentcomment_down', null=True, blank=True)

    def modify_points(self, added_points):
        self.puan += added_points
        self.blogpost.puan += added_points
        self.save()

    def save(self, *args, **kwargs):
        try:
            points = settings.POINTS_SETTINGS['GROUP_COMMENT']
        except KeyError:
            points = 0
        GrupIcerikleri.objects.get(pk=self.blogpost.id).modify_points(points)
        super(GrupIcerikleriComment, self).save(*args, **kwargs)


class Badges(models.Model):
    adi = models.CharField(max_length=75, default='', null=False)
    detay = models.TextField(max_length=340, default='', null=False)
    gorseli = models.ImageField(upload_to='badges/', null=False, default='/userprofiles/canberk2/628286_anonym_avatar_default_head_person_icon.png')
    uyeler = models.ManyToManyField(User, related_name='badges_kazananlar', null=True, blank=True)
    puan = models.PositiveIntegerField(default=0)


class Notification(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notification_user')
    title = models.CharField(max_length=30, blank=True)
    description = models.TextField(max_length=155, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    actor = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notification_actor', blank=True)
    badge = models.OneToOneField(Badges, related_name='notification_badge', on_delete=models.CASCADE, blank=True, null=True)
    badge_img = models.TextField(max_length=955, blank=True)
    description_badge = models.TextField(max_length=155, blank=True)
    puan_badge = models.PositiveIntegerField(default=0, blank=True)
    seen = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_user')
    bio = models.TextField(max_length=155, blank=True)
    ad = models.TextField(max_length=25, blank=True)
    soyad = models.TextField(max_length=25, blank=True)
    eposta = models.EmailField(max_length=254, null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.datetime.now)
    photo = models.ImageField(upload_to='pp/', blank=True, null=True, default='/userprofiles/canberk2/628286_anonym_avatar_default_head_person_icon.png')
    kapak = models.ImageField(upload_to='kapak/', blank=True, null=True, default='/userprofiles/canberk2/5559852.jpg')
    timestamp = models.DateField(auto_now_add=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank='True')
    takipettiklerim = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='takipci', blank='True')
    sonraoku = models.ManyToManyField(Content, related_name='sonra', blank='True')
    begendiklerim = models.ManyToManyField(Content, related_name='begendigim', blank='True')
    gruplarim = models.ManyToManyField(Group, related_name='katildigim', blank='True')
    verdigimoylar = models.ManyToManyField(PollQuestion, related_name='verdigimoylar', blank='True')
    rozetler = models.ManyToManyField(Badges, related_name='rozetler', blank='True')
    points = models.PositiveIntegerField(default=0, verbose_name="points")
    dailypoints = models.PositiveIntegerField(default=0, verbose_name="dailypoints")
    onayli = models.BooleanField(default=False)


    def modify_points(self, added_points):
        self.points += added_points
        self.save()

    def modify_daily_points(self, added_daily_points):
        self.dailypoints += added_daily_points
        self.save()

    def user_did_save(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)

    post_save.connect(user_did_save, sender=User)


class BlogPost(models.Model):
    icerik = models.TextField(max_length=200)
    olusturan = models.TextField(max_length=18)
    tarih = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    gorsel = models.ImageField(upload_to=nameFile3, blank=True, null=True)
    likes  = models.ManyToManyField(User, related_name='blogpost_like', null=True, blank=True)


class BlogPostComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name='blogpostcomments', on_delete=models.CASCADE, null=True, blank=True)
    yazan = models.TextField(max_length=18)
    body = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    yukari = models.ManyToManyField(User, related_name='blogcomment_up', null=True, blank=True)
    asagi = models.ManyToManyField(User, related_name='blogcomment_down', null=True, blank=True)


class HelpMessages(models.Model):
    sender = models.ForeignKey(User, related_name='help_user', on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    date_added = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)


class Conversation(models.Model):
    user_one = models.ForeignKey(User, related_name="user_one", on_delete=models.CASCADE, default='')
    user_two = models.ForeignKey(User, related_name="user_two", on_delete=models.CASCADE, default='')
    created_users = models.ManyToManyField(User, related_name='created', null=True, blank=True)
    deleted_by = models.ManyToManyField(User, related_name='deleted', null=True, blank=True)

    class Meta:
        unique_together = ('user_one', 'user_two')

    def save(self, *args, **kwargs):
        if not Conversation.objects.filter(user_one=self.user_two, user_two=self.user_one).exists():
            super(Conversation, self).save(*args, **kwargs)
        else:
            return ""


class Messages(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    conversation_key = models.ForeignKey(Conversation, related_name="conversation", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=240)
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)

class Hashtags(models.Model):
    tag = models.TextField(max_length=240)
    author = models.ForeignKey(User, related_name="tag_author", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.ManyToManyField(Content, related_name="tag_content", blank=True, null=True)
    blog_content = models.ManyToManyField(BlogPost, related_name="tag_blogcontent", blank=True, null=True)
    grup_content = models.ManyToManyField(GrupIcerikleri, related_name="tag_grupcontent", blank=True, null=True)
    comment = models.ManyToManyField(ContentComment, related_name="tag_commentcontent", blank=True, null=True)
    blog_comment = models.ManyToManyField(BlogPostComment, related_name="tag_blogcommentcontent", blank=True, null=True)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "Merhaba, şifreni sıfırlamak için TOKEN={} kodunu kullanabilirsin.".format(reset_password_token.key)

    send_mail(
        # title:
        "Wuubi - Şifrenizi Sıfırlayın.",
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

