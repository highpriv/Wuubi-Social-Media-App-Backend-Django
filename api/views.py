import datetime
from rest_framework import viewsets, status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db.models import Q
from backend import settings
from . import serializers
from .models import Content, Profile, Badges, Group, BlogPost, HelpMessages, BlogPostComment, ContentComment, GrupIcerikleri, \
    GrupIcerikleriComment, PersonalityResult, Messages, Conversation, PersonalityQuestion, PersonalityAnswer, Quiz, QuizAnswers, PollQuestion, \
    PollAnswer, Notification, Hashtags
from django.http import HttpResponse, Http404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from .serializers import ContentSerializer, UserSerializer, MessagesSerializer, HotContentSerializer, UserSerializerWithToken, GroupSerializer, \
    UserListesiSerializer, ProfileSerializer, BlogPostSerializer, TrendContentSerializer, BlogPostCommentSerializer, ChangePasswordSerializer, \
    ContentCommentSerializer, ContentMinimalSerializer, GrupIcerikleriSerializer, ConversationSerializer, BadgesSerializer, GrupIcerikleriCommentSerializer, PersonalityResultSerializer, \
    PersonalityQuestionSerializer, PersonalityAnswerSerializer, QuizSerializer, QuizAnswersSerializer, \
    PollAnswerSerializer, PollQuestionSerializer, PopularContentSerializer, PopulerProfilesSerializer, HashtagsSerializer, NotificationSerializer, HelpMessagesSerializer
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
import re
from django.core import serializers

from django.utils.functional import Promise
from django.utils.encoding import force_str
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super(LazyEncoder, self).default(obj)

def profile_detail_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404
    profile_obj = qs.first()
    context = {
        "username": username,
        "profile": profile_obj
    }
    return render(request, "profiles/detail.html", {"username": username})


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset


class PersonalityResultViewSet(viewsets.ModelViewSet):
    queryset = PersonalityResult.objects.all()
    serializer_class = PersonalityResultSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PersonalityQuestionViewSet(viewsets.ModelViewSet):
    queryset = PersonalityQuestion.objects.all()
    serializer_class = PersonalityQuestionSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PersonalityAnswerViewSet(viewsets.ModelViewSet):
    queryset = PersonalityAnswer.objects.all()
    serializer_class = PersonalityAnswerSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class QuizQuestionViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class QuizAnswerViewSet(viewsets.ModelViewSet):
    queryset = QuizAnswers.objects.all()
    serializer_class = QuizAnswersSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PollQuestionViewSet(viewsets.ModelViewSet):
    queryset = PollQuestion.objects.all()
    serializer_class = PollQuestionSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PollAnswerViewSet(viewsets.ModelViewSet):
    queryset = PollAnswer.objects.all()
    serializer_class = PollAnswerSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GrupIcerikleriViewSet(viewsets.ModelViewSet):

    serializer_class = GrupIcerikleriSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):

        user = self.request.user
        anonimus = self.request.user.is_anonymous

        if not anonimus:
            queryset = GrupIcerikleri.objects.filter(Q(grup__uyelerasil=user.id) | Q(grup__gizligrup='0'))
        else:
            queryset = GrupIcerikleri.objects.filter(grup__gizligrup='0')
        return queryset



class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('-puan')
    serializer_class = GroupSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = request.data
        kullanici = data["yoneticiler"]
        yoneticisayisi = Group.objects.filter(yoneticiler=kullanici).count()

        usser = Profile.objects.get(pk=kullanici)

        if yoneticisayisi > 4:
            response = {'message': 'En fazla 3 grupta yönetici olabilirsiniz.'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

        if Group.objects.filter(name=data["name"]).exists():
            response = {'message': 'Bu isimde bir grup zaten mevcut.'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            new_group = Group.objects.create(name=data["name"], description=data["description"], gizligrup=data["gizligrup"])
            new_group.uyelerasil.set(data["uyelerasil"])
            new_group.image_url = data["image_url"]
            new_group.yoneticiler.set(data["yoneticiler"])
            new_group.save()

            if not usser.rozetler.filter(pk=3).exists():
                points = settings.POINTS_SETTINGS['CREATE_GROUP']
                dailypoints = settings.POINTS_SETTINGS['CREATE_GROUP']
                usser.modify_points(points)
                usser.modify_points(dailypoints)

            usser.rozetler.add(3)

            rozet = Badges.objects.get(id=3)


            try:
                notificat = Notification.objects.create(title="Yeni bir başarım kazandın!",description_badge="{}".format(rozet.adi),puan_badge="{}".format(rozet.puan),badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                notificat.user.add(usser.user)
                return Response({"Başarılı": "Grup oluşturuldu"}, status=201)
            except:
                return Response({"Başarılı": "Grup oluşturuldu"}, status=201)


    def destroy(self, request, *args, **kwargs):
        foo_id = kwargs["pk"]
        query2 = Group.objects.get(pk=foo_id)
        query = query2

        me = request.user
        if query.yoneticiler.filter(pk=me.pk).exists():
            query.delete()
            GrupIcerikleri.objects.filter(grup=foo_id).delete()
            return Response({"Başarılı": "Grup karanlık uzayın boşluğuna doğru yavaşça süzülüyor..."}, status=200)
        else:
            return Response({"Hata": "Bu işlem için yetkin yok!"}, status=406)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def updategroup(request, id, *args, **kwargs):
    me = request.user
    grup2 = Group.objects.filter(id=id)
    grup = grup2.first()
    bilgilendirme = request.data['bilgilendirme']
    description = request.data['description']
    yoneticilerbefore = request.data['yoneticiler']
    gizligrup = request.data['gizligrup']
    grup.bilgilendirme = bilgilendirme
    grup.description = description
    grup.gizligrup = gizligrup

    if grup.yoneticiler.count() < 5:
        arr = [x.strip() for x in yoneticilerbefore.strip('[]').split(',')]
        for y in arr:
            gruplink = grup.name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("İ", "i").replace("ö", "o").replace("ç", "c").replace(" ", "-").replace(".", "")
            notificat = Notification.objects.create(title="tarafından '{}' grubuna yönetici atandın.".format(grup.name), description="/g/{}".format(gruplink))
            notificat.actor.add(me.id)
            notificat.user.add(y)
            grup.yoneticiler.add(y)
    else:
        response = {'message': 'Yönetici sınırlamasına ulaşıldı.'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not grup.yoneticiler.filter(pk=me.pk).exists():
        response = {'message': 'Yönetici olmadığınız bir grubu düzenleyemezsiniz.'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    if not re.match("^[01]*$", gizligrup):
        response = {'message': 'Parametre hatası!'}
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)




    grup.save()
    response = {'message': 'grup düzenlendi'}
    return Response(response, status=status.HTTP_200_OK)


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def deleteuser(request, id, *args, **kwargs):

    if request.user:
        user2 = User.objects.filter(id=id)
        user = user2.first()
        user.delete()
        response = {'message': 'üye silindi ' + request.user.username}
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {'message': 'yetkisiz işlem' + request.user.username}
        return Response(response, status=status.HTTP_403_FORBIDDEN)



class BlogPostCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogPostComment.objects.all()
    serializer_class = BlogPostCommentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ContentCommentViewSet(viewsets.ModelViewSet):
    queryset = ContentComment.objects.all()
    serializer_class = ContentCommentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AllUsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserListesiSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
            queryset = User.objects.exclude(is_superuser='True')
            return queryset


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    myprofilim = Profile.objects.get(user=me.id)
    other_user_qs = User.objects.filter(username=username)

    idcek = User.objects.get(username=username).id

    if me.username == username:
        my_followers = myprofilim.followers.all()
        return Response({"followers": my_followers.count()}, status=200)
    other = other_user_qs.first()
    profilex = Profile.objects.filter(user=idcek).first()
    myprofile = Profile.objects.filter(user=me).first()
    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "follow":
        profilex.followers.add(me)
        myprofile.takipettiklerim.add(idcek)

        notificat = Notification.objects.create(title="seni takip etmeye başladı.",description="/u/{}".format(username))
        notificat.actor.add(me.id)
        notificat.user.add(idcek)

        if profilex.followers.count() > 99:
            profilex.rozetler.add(4)
            rozet = Badges.objects.get(id=4)
            notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
            notificat.user.add(idcek)
    elif action == "unfollow":
        profilex.followers.remove(me)
        myprofile.takipettiklerim.remove(idcek)
    else:
        pass
    current_followers_qs = profilex.followers.all()
    return Response({"followers":current_followers_qs.count()}, status=200)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.exclude(user=1)
    serializer_class = ProfileSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['POST'])
    def updateprofile(self, request, pk=None):
        user = request.user
        kullanici = User.objects.get(username=user.username)
        bio = request.data['bio']
        ad = request.data['ad']
        eposta = request.data['eposta']
        username = request.data['username']
        birth_date = request.data['birth_date']
        location = request.data['location']
        profil = Profile.objects.get(user=user)
        profil.bio = bio
        profil.eposta = eposta
        profil.ad = ad
        kullanici.username = username
        profil.location = location
        profil.birth_date = birth_date

        if Profile.objects.exclude(user=request.user).filter(eposta=request.data['eposta']).exists():
            response ={'message':'Bu mail adresi ile hesap bulunuyor.'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

        if request.data['kapak'] != 'empty':
            kapak = request.data['kapak']
            profil.kapak = kapak

        if request.data['photo'] != 'empty':
            photo = request.data['photo']
            profil.photo = photo

        if User.objects.exclude(username=request.user.username).filter(username=request.data['username']).exists():
            response = {'message': 'Bu kullanıcı adı ile hesap bulunuyor.'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

        kullanici.save()
        profil.save()
        response = {'message':'its ok'}
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def blogpost_like(request, id, *args, **kwargs):

    me = request.user
    icerik2 = BlogPost.objects.filter(id=id)
    icerik = icerik2.first()
    creator = User.objects.get(username=icerik.olusturan)

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "like":
        notificat = Notification.objects.create(title="profil paylaşımını beğendi.",description="/u/{}".format(creator.username))
        notificat.actor.add(me.id)
        notificat.user.add(creator.id)
        icerik.likes.add(me)

    elif action == "unlike":
        icerik.likes.remove(me)
    else:
        pass
    begenisayisi = icerik.likes.all()
    return Response({"begeni":begenisayisi.count()}, status=400)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def blogcomment_up(request, id, *args, **kwargs):

    me = request.user

    icerik2 = BlogPostComment.objects.filter(id=id)
    icerik = icerik2.first()


    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "up":
        if icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
        elif icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
            icerik.yukari.add(me)
        else:
            icerik.yukari.add(me)
    elif action == "down":
        if icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
        elif icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
            icerik.asagi.add(me)
        else:
            icerik.asagi.add(me)
    else:
        pass
    sayi = icerik.yukari.all()
    return Response({"yukari": sayi.count()}, status=400)





@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def contentcomment_up(request, id, *args, **kwargs):

    me = request.user

    icerik2 = ContentComment.objects.filter(id=id)
    icerik = icerik2.first()


    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "up":
        if icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
        elif icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
            icerik.yukari.add(me)
        else:
            icerik.yukari.add(me)
    elif action == "down":
        if icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
        elif icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
            icerik.asagi.add(me)
        else:
            icerik.asagi.add(me)
    else:
        pass
    sayi = icerik.yukari.all()
    return Response({"yukari": sayi.count()}, status=400)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'degisti',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def sonraokuyaekle(request, id, *args, **kwargs):

    mee=request.user
    me = Profile.objects.get(user=mee.id)
    icerik2 = Content.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "ekle":
        me.sonraoku.add(id)
        icerik.okuyacaklar.add(mee)
    elif action == "kaldir":
        me.sonraoku.remove(id)
        icerik.okuyacaklar.remove(mee)
    else:
        pass
    return Response({"okunacaklar":me.sonraoku.count()}, status=400)




@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def begeniyeekle(request, id, *args, **kwargs):

    mee=request.user
    me = Profile.objects.get(user=mee.id)
    icerik2 = Content.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "ekle":
        me.begendiklerim.add(id)
        icerik.begenenler.add(mee)
        kisaurl = icerik.title.replace(' ', '-').replace('.','').lower()
        notificat = Notification.objects.create(title="ürettiğin içeriği beğendi.",description="/i/{}".format(kisaurl))
        notificat.actor.add(mee.id)
        notificat.user.add(icerik.olusturanid)
    elif action == "kaldir":
        me.begendiklerim.remove(id)
        icerik.begenenler.remove(mee)
    else:
        pass
    return Response({"begendiklerim":me.begendiklerim.count()}, status=400)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def grupislemleri(request, id, *args, **kwargs):

    me2 = request.user
    me = Profile.objects.get(user=me2)
    mee = request.user
    grup2 = Group.objects.filter(id=id)
    grup = grup2.first()
    data = {}
    try:
        data = request.data
    except:
        pass

    action = data.get("action")
    if grup.gizligrup=="0":
        if action == "katil":
            me.gruplarim.add(id)
            grup.uyelerasil.add(mee)
            return Response({"gruba katıldın"}, status=200)
        elif action == "cik":
            me.gruplarim.remove(id)
            grup.uyeler.remove(mee)
            grup.uyelerasil.remove(mee)
            return Response({"gruptan çıktın"}, status=200)

    if grup.gizligrup == "1":
        if action == "katil":
            me.gruplarim.add(id)
            grup.uyeler.add(mee)
            return Response({"katılma isteğin gönderildi"}, status=200)
        elif action == "cik":
            me.gruplarim.remove(id)
            grup.uyeler.remove(mee)
            grup.uyelerasil.remove(mee)
            return Response({"gruptan çıktın. tekrar girmen için istek gönder."}, status=200)
    else:
        return Response({"tanımsız grup türü. destek alın."}, status=200)




@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def yoneticieklekaldir(request, id, *args, **kwargs):

    me = request.user
    grup2 = Group.objects.filter(id=id)
    grup = grup2.first()
    kullanici = request.data['kullanici']

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "ekle":
        if grup.yoneticiler.filter(pk=me.pk).exists():
            grup.yoneticiler.add(kullanici)
        else:
            return Response({"bu işlem için yetkiniz yok"}, status=406)
    elif action == "cik":
        if grup.yoneticiler.filter(pk=me.pk).exists():
            grup.yoneticiler.remove(kullanici)
        else:
            return Response({"bu işlem için yetkiniz yok"}, status=406)
    else:
        return Response({"hata!"}, status=406)
    return Response({"başarılı"}, status=200)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def grcontentbegen(request, id, *args, **kwargs):

    me = request.user
    mee=request.user
    icerik2 = GrupIcerikleri.objects.filter(id=id)
    icerik = icerik2.first()
    grubu = icerik.grup
    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")

    if grubu.uyelerasil.filter(pk=me.pk).exists():
        if action == "ekle":
            icerik.begenenler.add(mee)
            return Response({"başarılı"}, status=200)
        elif action == "kaldir":
            icerik.begenenler.remove(mee)
            return Response({"başarılı"}, status=200)
        else:
            return Response({"buna yetkin bulunmuyor."}, status=406)
    else:
        return Response({"buna yetkin bulunmuyor"}, status=406)


class GrupIcerikleriCommentViewSet(viewsets.ModelViewSet):
    queryset = GrupIcerikleriComment.objects.all()
    serializer_class = GrupIcerikleriCommentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class BadgesViewSet(viewsets.ModelViewSet):
    queryset = Badges.objects.all()
    serializer_class = BadgesSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def create(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def save(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def create(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def grupcomment_up(request, id, *args, **kwargs):

    me = request.user

    icerik2 = GrupIcerikleriComment.objects.filter(id=id)
    icerik = icerik2.first()

    idsi = icerik.blogpost
    grubu = idsi.grup
    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "up":
        if icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
        elif icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
            icerik.yukari.add(me)
        else:
            icerik.yukari.add(me)
    elif action == "down":
        if icerik.asagi.filter(pk=me.pk).exists():
            icerik.asagi.remove(me)
        elif icerik.yukari.filter(pk=me.pk).exists():
            icerik.yukari.remove(me)
            icerik.asagi.add(me)
        else:
            icerik.asagi.add(me)
    else:
        pass
    sayi = icerik.yukari.all()
    return Response({"yukari": sayi.count()}, status=400)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def uyekabulred(request, id, *args, **kwargs):

    me = request.user
    grup2 = Group.objects.filter(id=id)
    grup = grup2.first()
    kullanici = request.data['kullanici']

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "kabul":
        if grup.yoneticiler.filter(pk=me.pk).exists():
            if grup.uyeler.filter(pk=kullanici).exists():
                grup.uyelerasil.add(kullanici)
                grup.uyeler.remove(kullanici)
                gruplink = grup.name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş",
                                                                                                           "s").replace(
                    "İ", "i") \
                    .replace("ö", "o").replace("ç", "c").replace(" ", "-").replace(".", "")
                notificat = Notification.objects.create(title="tarafından '{}' grubuna katılım isteğin onaylandı.".format(grup.name),description="/g/{}".format(gruplink))
                notificat.user.add(kullanici)
                notificat.actor.add(me.id)

            else:
                return Response({"bu üyenin katılım daveti yok"}, status=406)
        else:
            return Response({"bu işlem için yetkiniz yok"}, status=406)
    elif action == "red":
        if grup.yoneticiler.filter(pk=me.pk).exists():
            if grup.uyeler.filter(pk=kullanici).exists():
                grup.uyeler.remove(kullanici)
            else:
                return Response({"bu üyenin katılım daveti yok"}, status=406)
        else:
            return Response({"bu işlem için yetkiniz yok"}, status=406)
    else:
        return Response({"hata!"}, status=406)
    return Response({"başarılı"}, status=200)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def uyekaldir(request, id, *args, **kwargs):

    me = request.user
    grup2 = Group.objects.filter(id=id)
    grup = grup2.first()
    kullanici = request.data['kullanici']

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "cikart":
        if grup.yoneticiler.filter(pk=me.pk).exists():
            grup.uyeler.remove(kullanici)
            grup.uyelerasil.remove(kullanici)
        else:
            return Response({"bu işlem için yetkiniz yok"}, status=406)
    else:
        return Response({"hata!"}, status=406)
    return Response({"başarılı"}, status=200)



@api_view(['POST', 'GET'])
@permission_classes((AllowAny, ))
def testgetir(request, id, *args, **kwargs):
    icerik = Content.objects.get(id=id)

    if icerik:
        qs = serializers.serialize("json", icerik.test.all())
        return HttpResponse(qs, content_type="text/json-comment-filtered")
    else:
        return Response({"içerik bulunamadı"}, status=404)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def testgetirq(request, id, *args, **kwargs):
    icerik = Content.objects.get(id=id)

    if icerik:
        qs = serializers.serialize("json", icerik.quiz.all())
        return HttpResponse(qs, content_type="text/json-comment-filtered")
    else:
        return Response({"içerik bulunamadı"}, status=404)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def testhesapla(request):

    def most_frequent(List):
        counter = 0
        num = List[0]

        for i in List:
            curr_frequency = List.count(i)
            if curr_frequency > counter:
                counter = curr_frequency
                num = i

        return num

    cevaplar = request.data['cevaplar']
    List = cevaplar.split(',')
    result = most_frequent(List)

    return Response({result}, status=200)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def polloyver(request, id, *args, **kwargs):
    me = request.user
    myprofile = Profile.objects.get(user=me.id)

    yanitgetir = PollAnswer.objects.filter(id=id)
    yanit = yanitgetir.first()

    questions = PollQuestion.objects.filter(answer=id)
    sorusu = questions.first()

    yanitgrubu = PollQuestion.objects.filter(id=sorusu.id)
    yanitgrubur = yanitgrubu.first()
    yanitgrubulast = yanitgrubur.answer.all()

    if yanit.katilanlar.filter(id=me.id).exists():
        yanit.katilanlar.remove(me)
        myprofile.verdigimoylar.remove(sorusu)

    else:

        if myprofile.verdigimoylar.filter(id=sorusu.id):
            for x in yanitgrubulast:
                x.katilanlar.remove(me)
            yanit.katilanlar.add(me)

        else:
            myprofile.verdigimoylar.add(sorusu)
            yanit.katilanlar.add(me)

    return Response({"followers":questions.count()}, status=200)



### Popüler Üyeler ###

class PopulerProfilesViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('-dailypoints')
    serializer_class = PopulerProfilesSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def notificationcheck(request, *args, **kwargs):

    me2 = request.user
    me = Notification.objects.filter(user=me2).filter(seen=False)

    return Response({"notification": me.count()}, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def setallseen(request, *args, **kwargs):

    me2 = request.user
    me = Notification.objects.filter(user=me2)

    for noti in me:
        noti.seen = True
        noti.save()


    return Response({"notification": me.count()}, status=200)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        me = self.request.user
        queryset = Notification.objects.filter(user=me.id).order_by('-timestamp')
        return queryset


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        me = self.request.user
        queryset = Conversation.objects.filter(Q(user_one=me.id) | Q(user_two=me.id))
        return queryset


    def create(self, request, *args, **kwargs):
        data = request.data
        me = self.request.user

        user_one = data["user_one"]
        user_one_int = int(user_one)
        user_two = data["user_two"]

        usertwo = User.objects.get(id=user_two)

        if not Conversation.objects.filter(Q(user_one=me, user_two=usertwo) | Q(user_one=usertwo, user_two=me)).exists():
            if user_one_int==me.id:
                new_conversation = Conversation.objects.create(user_one=me, user_two=usertwo)
                new_conversation.created_users.add(me.id)
                new_conversation.save()
                response = {'Konuşma': 'Konuşma oluşturuldu!'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'Konuşma': 'Başkası adına konuşma oluşturamazsın!'}
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            conversat = Conversation.objects.filter(Q(user_one=me, user_two=usertwo) | Q(user_one=usertwo, user_two=me))
            conversation = conversat.first()
            conversation.deleted_by.remove(me.id)
            conversation.created_users.add(me.id)
            response = {'Konuşma': 'Konuşmaya eklendin!'}
            return Response(response, status=status.HTTP_200_OK)





class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_queryset(self):
        me = self.request.user
        queryset = Messages.objects.filter(Q(sender=me.id) | Q(reciever=me.id)).filter(owner=me.id).order_by('timestamp')
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        me = self.request.user

        sender_old = data["sender"]
        sender = User.objects.get(id=sender_old)

        conversation_key_old = data["conversation_key"]
        convid = Conversation.objects.get(id=conversation_key_old)

        reciever_old = data["reciever"]
        reciever = User.objects.get(id=reciever_old)

        msg_content = data["msg_content"]

        conversation_old = Conversation.objects.filter(Q(user_one=me.id, user_two=reciever.id) | Q(user_one=reciever.id, user_two=me.id) | Q(user_one=me.id, user_two=sender.id) | Q(user_one=sender.id, user_two=me.id))
        conversation = conversation_old.first()


        if conversation_old.exists():
            if sender.id == me.id:
                if sender != reciever:
                    new_message = Messages.objects.create(conversation_key=convid, msg_content=msg_content,
                                                          sender=sender, reciever=reciever, owner=sender)
                    new_message.save()

                    new_message_scnd = Messages.objects.create(conversation_key=convid, msg_content=msg_content,
                                                          sender=sender, reciever=reciever, owner=reciever)
                    new_message_scnd.save()

                    conversation.created_users.add(sender.id)
                    conversation.created_users.add(reciever.id)
                    conversation.save()

                    response = {'Mesaj': 'Gönderildi!.'}
                    return Response(response, status=status.HTTP_200_OK)

                else:
                    response = {'Mesaj': 'Kendine mesaj gönderemezsin!'}
                    return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                response = {'Mesaj': 'Başkası adına mesaj gönderemezsin!'}
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:

            new_conversation = Conversation.objects.create(user_one=sender, user_two=reciever)
            new_conversation.created_users.add(sender.id)
            new_conversation.created_users.add(reciever.id)
            new_conversation.save()

            if sender.id == me.id:
                if sender != reciever:
                    new_message = Messages.objects.create(conversation_key=convid, msg_content=msg_content,
                                                          sender=sender, reciever=reciever)
                    new_message.save()


                    response = {'Mesaj': 'Gönderildi!.'}
                    return Response(response, status=status.HTTP_200_OK)

                else:
                    response = {'Mesaj': 'Kendine mesaj gönderemezsin!'}
                    return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                response = {'Mesaj': 'Başkası adına mesaj gönderemezsin!'}
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def delete_conversation(request, id, *args, **kwargs):

    me = request.user

    conversation_s = Conversation.objects.filter(id=id)
    conversation = conversation_s.first()
    conversation.deleted_by.add(me)

    Messages.objects.filter(conversation_key=id).filter(owner=me).delete()

    return Response({"Konuşma silindi!"}, status=200)




class HelpMessagesViewSet(viewsets.ModelViewSet):
    queryset = HelpMessages.objects.all()
    serializer_class = HelpMessagesSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        me = self.request.user
        queryset = HelpMessages.objects.filter(sender=me.id)
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def emoji_ver(request, id, *args, **kwargs):

    me = request.user
    icerik2 = Content.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass
    action = data.get("action")
    if action == "endiseli":
        icerik.endiseli.add(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "komik":
        icerik.endiseli.remove(me)
        icerik.komik.add(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "sinirli":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.add(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "alkis":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.add(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "saskin":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.add(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "uzgun":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.add(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.remove(me)
    elif action == "igrenc":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.add(me)
        icerik.sevdim.remove(me)
    elif action == "sevdim":
        icerik.endiseli.remove(me)
        icerik.komik.remove(me)
        icerik.sinirli.remove(me)
        icerik.alkis.remove(me)
        icerik.saskin.remove(me)
        icerik.uzgun.remove(me)
        icerik.igrenc.remove(me)
        icerik.sevdim.add(me)
    else:
        pass
    mesaj="Emoji verildi!"
    return Response({"Tamam":mesaj}, status=200)


class HashtagsViewSet(viewsets.ModelViewSet):
    queryset = Hashtags.objects.all()
    serializer_class = HashtagsSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get', 'post']

    def get_queryset(self):
        me = self.request.user
        queryset = Hashtags.objects.all()
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)



class ContentMinimalViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentMinimalSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get']

    def get_queryset(self):
        me = self.request.user
        queryset = Content.objects.filter(yayinda=True)
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def post(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)


class PopularContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = PopularContentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get']

    def get_queryset(self):
        me = self.request.user
        queryset = Content.objects.filter(yayinda=True)
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def post(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)


class HotContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = HotContentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get']

    def get_queryset(self):
        me = self.request.user
        queryset = Content.objects.filter(yayinda=True)
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def post(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)



class TrendContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = TrendContentSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ['get']

    def get_queryset(self):
        me = self.request.user
        queryset = Content.objects.filter(yayinda=True)
        return queryset

    def update(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def put(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def delete(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

    def post(self, validated_data):
        return Response({"Tanımsız işlem."}, status=400)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def blogpost_sil(request, id, *args, **kwargs):

    me = request.user
    icerik2 = BlogPost.objects.filter(id=id)
    icerik = icerik2.first()
    if icerik.olusturan == me.username:
        icerik.delete()
        mesaj = "İçerik Silindi!"
        return Response({"Başarılı": mesaj}, status=200)
    else:
        mesaj = "Hata!"
        return Response({"Yetkisiz": mesaj}, status=401)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def blogpost_edit(request, id, *args, **kwargs):

    me = request.user
    icerik2 = BlogPost.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass

    new_body = data.get("content")
    new_img = data.get("gorsel")

    if not new_body:
        mesaj = "Yeni içerik yok"
        return Response({"Tanımsız Değer": mesaj}, status=406)

    if icerik.olusturan == me.username:

        if new_img:
            icerik.icerik = new_body
            icerik.gorsel = new_img
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)

        if not new_body:
            icerik.gorsel = new_img
            icerik.save()
            mesaj = "İçerik değiştirildi"

        if not new_img:
            icerik.icerik = new_body
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)
    else:
        mesaj = "Hata!"
        return Response({"Yetkisiz": mesaj}, status=401)



@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def content_edit(request, id, *args, **kwargs):

    me = request.user
    icerik2 = Content.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass

    new_title = data.get("title")
    new_ozet = data.get("ozet")
    new_thumbnail = data.get("thumbnail")
    new_vucut = data.get("vucut")

    new_liste = data.get("liste")
    new_listeicerik = data.get("listeicerik")
    new_listegorsel = data.get("listegorsel")

    new_test = data.get("test")
    new_quiz = data.get("quiz")
    new_poll = data.get("poll")


    if icerik.olusturan == me.username:

        if new_title:
            icerik.title = new_title

        if new_thumbnail:
            print("geldi")
            icerik.thumbnail = new_thumbnail

        if new_vucut:
            icerik.vucut = new_vucut

        if new_ozet:
            icerik.ozet = new_ozet

        if new_liste:
            icerik.liste = new_liste

        if new_listeicerik:
            icerik.listeicerik = new_listeicerik

        if new_listegorsel:
            icerik.listegorsel = new_listegorsel

        if new_test:
            icerik.test.set(new_test)

        if new_quiz:
            icerik.quiz.set(new_quiz)

        if new_poll:
            icerik.poll.set(new_poll)

        icerik.save()
        mesaj = "İçerik değiştirildi"
        return Response({"Güncellendi": mesaj}, status=200)

    else:
        mesaj = "Hata!"
        return Response({"Yetkisiz": mesaj}, status=401)




@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def test_question_edit(request, id, *args, **kwargs):

    me = request.user
    icerik2 = PersonalityQuestion.objects.filter(id=id)
    icerik = icerik2.first()

    data = {}
    try:
        data = request.data
    except:
        pass

    new_title = data.get("title")
    new_body = data.get("body")
    new_img = data.get("img")


    if icerik.olusturan == me.username:

        if new_img:
            icerik.title = new_title
            icerik.body = new_body
            icerik.img = new_img
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)

        if not new_img:
            icerik.title = new_title
            icerik.body = new_body
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)

    else:
        mesaj = "Hata!"
        return Response({"Yetkisiz": mesaj}, status=401)




@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def test_answer_edit(request, id, *args, **kwargs):

    me = request.user
    icerik = PersonalityAnswer.objects.get(id=id)

    data = {}
    try:
        data = request.data
    except:
        pass

    new_result = data.get("result")
    new_body = data.get("body")
    new_img = data.get("img")

    qst = PersonalityQuestion.objects.filter(answer=id).last()

    if qst.olusturan == me.username:

        if new_img:
            icerik.body = new_body
            icerik.img = new_img
            if new_result:
                new_one = PersonalityResult.objects.get(sonuc=new_result)
                icerik.result=new_one
                icerik.save()
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)

        if not new_img:
            icerik.img = new_img
            icerik.body = new_body
            if new_result:
                new_one = PersonalityResult.objects.get(sonuc=new_result)
                icerik.result=new_one
                icerik.save()
            icerik.save()
            mesaj = "İçerik değiştirildi"
            return Response({"Güncellendi": mesaj}, status=200)

    else:
        mesaj = "Hata!"
        return Response({"Yetkisiz": mesaj}, status=401)



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def set_conversation_seen(request, id, *args, **kwargs):

    me = request.user

    messages = Messages.objects.filter(conversation_key=id)

    for msg in messages:

         if msg.sender==me:
            pass

         elif msg.reciever==me:
             msg.seen = True
             msg.save()

         else:
            pass

    return Response({"yes!"}, status=200)



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JSONWebTokenAuthentication,))
def check_new_msg(request, *args, **kwargs):

    me = request.user

    messages = Messages.objects.filter(reciever=me, owner=me, seen=False)

    new_msg = messages.count()



    return Response({new_msg}, status=200)
