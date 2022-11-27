import datetime
import pytz
utc = pytz.UTC
from rest_framework_jwt.serializers import User
from .models import Content, Profile, BlogPost, BlogPostComment, ContentComment, Group, GrupIcerikleri, \
    GrupIcerikleriComment, PersonalityResult, PersonalityQuestion, PersonalityAnswer, QuizAnswers, Quiz, PollQuestion, \
    PollAnswer, Notification, Badges, Conversation, Messages, HelpMessages, Hashtags
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
import re
from django.utils.text import slugify
from unicode_tr import unicode_tr

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ContentSerializer(serializers.ModelSerializer):
    okuyacaklar = serializers.SlugRelatedField(queryset=Content.objects.all(), many=True, slug_field="username")
    okuyacaksin = serializers.SerializerMethodField('okucheck')
    begenenler = serializers.SlugRelatedField(queryset=Content.objects.all(), many=True, slug_field="username")
    begendinmi = serializers.SerializerMethodField('begenicheck')
    hashtags = serializers.SerializerMethodField('hashtaggenerator')
    count = serializers.SerializerMethodField('viewcounter')
    hot = serializers.SerializerMethodField('hotmu')
    popular = serializers.SerializerMethodField('popularmi')
    trend = serializers.SerializerMethodField('trendmi')
    kategori_slug = serializers.SerializerMethodField('kategorisluggen')

    endiseliyim = serializers.SerializerMethodField('endisechk')
    endiseliprc = serializers.SerializerMethodField('endiselipercent')

    guldum = serializers.SerializerMethodField('guldumchk')
    guldumprc = serializers.SerializerMethodField('guldumpercent')

    kizdim = serializers.SerializerMethodField('kizdimchk')
    kizdimprc = serializers.SerializerMethodField('kizdimpercent')

    alkisladim = serializers.SerializerMethodField('alkisladimchk')
    alkisladimprc = serializers.SerializerMethodField('alkisladimpercent')

    sasirdim = serializers.SerializerMethodField('sasirdimchk')
    sasirdimprc = serializers.SerializerMethodField('sasirdimpercent')

    uzuldum = serializers.SerializerMethodField('uzuldumchk')
    uzuldumprc = serializers.SerializerMethodField('uzuldumpercent')

    igrendim = serializers.SerializerMethodField('igrendimchk')
    igrendimprc = serializers.SerializerMethodField('igrendimpercent')

    begendim = serializers.SerializerMethodField('begendimchk')
    begendimprc = serializers.SerializerMethodField('begendimpercent')

    def kategorisluggen(self, obj):
        try:
            slug_x = str(obj.kategori)
            slug = slugify(slug_x)
            return slug
        except:
            return "hata"


    def endisechk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.endiseli.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"


    def endiselipercent(self,obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.endiseli.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0


    def guldumchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.komik.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"


    def guldumpercent(self,obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.komik.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def kizdimchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.sinirli.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def kizdimpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.sinirli.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def alkisladimchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.alkis.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def alkisladimpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.alkis.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def sasirdimchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.saskin.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def sasirdimpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.saskin.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def uzuldumchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.uzgun.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def uzuldumpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.uzgun.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def igrendimchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.igrenc.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def igrendimpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.igrenc.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def begendimchk(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.sevdim.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"


    def begendimpercent(self, obj):
        toplam = obj.endiseli.count() + obj.komik.count() + obj.sinirli.count() + obj.alkis.count() + obj.saskin.count() + obj.uzgun.count() + obj.igrenc.count() + obj.sevdim.count()

        obje = obj.sevdim.count()

        if toplam > 0:
            yuzdehesabi_bf = obje / toplam
            yuzdehesabi = yuzdehesabi_bf * 100
            return yuzdehesabi
        else:
            return 0

    def viewcounter(self, obj):
        blog_object = Content.objects.get(id=obj.id)
        blog_object.goruntulenme = blog_object.goruntulenme + 1
        yazarprofili = Profile.objects.get(user=blog_object.olusturanid)

        if blog_object.goruntulenme > 999:
            yazarprofili.rozetler.add(5)

            rozet = Badges.objects.get(id=5)
            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        if blog_object.sliderde:
            yazarprofili.rozetler.add(6)

            rozet = Badges.objects.get(id=6)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        sayisi = Content.objects.filter(olusturanid=obj.olusturanid).count()
        if sayisi > 2:
            yazarprofili.rozetler.add(7)
            rozet = Badges.objects.get(id=7)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        if blog_object.begenenler.count() > 50:
            yazarprofili.rozetler.add(8)
            rozet = Badges.objects.get(id=8)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        if blog_object.okuyacaklar.count() > 50:
            yazarprofili.rozetler.add(9)  ## ilgi çekici içerik en az 50 okuyacak kişi ##
            rozet = Badges.objects.get(id=9)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        if blog_object.begenenler.count() > 50:
            yazarprofili.rozetler.add(10)  ## hot içerik rozeti 24 saatte 1000 den fazla okuma ##
            rozet = Badges.objects.get(id=10)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""

        blog_comments = ContentComment.objects.filter(post=blog_object.id)
        if blog_comments.count() > 50:
            yazarprofili.rozetler.add(11)  ## trend içerik rozeti en az 50 yorum##
            rozet = Badges.objects.get(id=11)

            if not Notification.objects.filter(user=blog_object.olusturanid, badge=rozet).exists():
                try:
                    notificat = Notification.objects.create(title="Yeni bir başarım kazandın!", description_badge="{}".format(rozet.adi), puan_badge="{}".format(rozet.puan), badge_img="http://localhost:8000/images/{}".format(rozet.gorseli), badge=rozet)
                    notificat.user.add(blog_object.olusturanid)
                    notificat.save()
                except:
                    return ""
        blog_object.save()
        return blog_object.goruntulenme

    def hotmu(self, obj):

        try:
            blog_object = Content.objects.get(id=obj.id)

            time_threshold = blog_object.created_at + datetime.timedelta(hours=24)

            now = datetime.datetime.now().replace(tzinfo=utc)

            if (time_threshold > now):
                if blog_object.goruntulenme > 999:
                    return "true"
                else:
                    return "false"
            else:
                return "false"

        except:
            return "hata"

    def popularmi(self, obj):

        try:
            blog_object = Content.objects.get(id=obj.id)

            if blog_object.begenenler.count() > 1:
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def trendmi(self, obj):
        try:
            if ContentComment.objects.filter(post=obj.id).exists():
                blog_comments = ContentComment.objects.filter(post=obj.id)
                if blog_comments.count() > 3:
                    return "true"
                else:
                    return "false"
            else:
                return "false"
        except:
            return "hata"

    def hashtaggenerator(self, obj):
            blog_object = Content.objects.get(id=obj.id)
            userx = User.objects.get(id=blog_object.olusturanid)

            icerikler_old = blog_object.vucut
            icerikler = icerikler_old.replace('&uuml;', 'ü').replace('&Uuml;', 'ü').replace('&Ccedil;', 'ç').replace('&ccedil;', 'ç').replace('&ouml;', 'ö').replace('&Ouml;', 'ö').lower()
            step_0 = re.findall(r"#(\w+)", icerikler)
            blog_object.hashtagler = step_0
            blog_object.save()

            for ste in step_0:
               if not Hashtags.objects.filter(tag=ste, author=userx, content=blog_object).exists():
                   tago = Hashtags.objects.create(tag=ste, author=userx)
                   tago.content.add(blog_object)
                   tago.save()
               else:
                   return""


            listeler = blog_object.listeicerik.replace('&uuml;', 'ü').replace('&Uuml;', 'ü').replace('&Ccedil;', 'ç').replace('&ccedil;', 'ç').replace('&ouml;', 'ö').replace('&Ouml;', 'ö').lower()
            step_1 = re.findall("#([a-zA-Z0-9_]{1,50})", listeler)
            blog_object.hashtagler = step_1

            for ste in step_1:
               if not Hashtags.objects.filter(tag=ste, author=userx, content=blog_object).exists():
                   tago = Hashtags.objects.create(tag=ste, author=userx)
                   tago.content.add(blog_object)
                   tago.save()
               else:
                   return""

            blog_object.save()
            return step_0 + step_1


    def okucheck(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.okuyacaklar.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def begenicheck(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.begenenler.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    ##def kisaurl(self, obj):
    #    try:
    #        return obj.title.replace(' ', '-').replace('.', '').lower()
    #    except:
    #        return "hata"

    class Meta:
        model = Content
        fields = (
        'id', 'title', 'yayinda', 'ozet', 'kategori_slug', 'hot', 'trend', 'popular', 'olusturanid', 'poll', 'test', 'quiz', 'count', 'hashtags',
        'hashtagler', 'kategori', 'count', 'begenenler', 'begendinmi', 'sliderde', 'created_at', 'kisalink', 'vucut',
        'olusturan', 'thumbnail', 'endiseliyim','endiseliprc','guldum', 'guldumprc','kizdim', 'kizdimprc','alkisladim', 'alkisladimprc',
        'sasirdim', 'sasirdimprc','uzuldum','uzuldumprc','igrendim', 'igrendimprc','begendim', 'begendimprc','liste', 'listeicerik', 'listegorsel', 'okuyacaksin', 'okuyacaklar', 'goruntulenme')




class ContentMinimalSerializer(serializers.ModelSerializer):

    kategori_slug = serializers.SerializerMethodField('kategorisluggen')
    begenisayisi = serializers.SerializerMethodField('begeni_calculator')
    begendinmi = serializers.SerializerMethodField('begenicheck')
    okuyacaksayisi = serializers.SerializerMethodField('okuyacak_calculator')
    okuyacaksin = serializers.SerializerMethodField('okucheck')

    def okucheck(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.okuyacaklar.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"

    def begenicheck(self, obj):
        try:
            request = self.context.get('request', None)
            if obj.begenenler.filter(username=request.user.username).exists():
                return "true"
            else:
                return "false"
        except:
            return "hata"


    def kategorisluggen(self, obj):
        try:
             slug_x = str(obj.kategori)
             slug = slugify(slug_x)
             return slug
        except:
            return "hata"

    def okuyacak_calculator(self, obj):
        try:
             readers = obj.okuyacaklar
             return readers.count()
        except:
            return "hata"

    def begeni_calculator(self, obj):
        try:
             readers = obj.begenenler
             return readers.count()
        except:
            return "hata"

    class Meta:
        model = Content
        fields = (
        'id', 'title', 'yayinda', 'ozet', 'kategori_slug', 'olusturanid',
        'kategori', 'begenisayisi', 'begendinmi', 'sliderde', 'created_at', 'kisalink',
        'olusturan', 'thumbnail', 'okuyacaksin', 'okuyacaksayisi', 'goruntulenme')



class PopularContentSerializer(serializers.ModelSerializer):

    popular = serializers.SerializerMethodField('popularmi')


    def popularmi(self, obj):

        try:
            blog_object = Content.objects.get(id=obj.id)

            if blog_object.begenenler.count() > 1:
                return "true"
            else:
                return "false"
        except:
            return "hata"
    class Meta:
        model = Content
        fields = ('id', 'title', 'yayinda', 'popular', 'ozet', 'olusturanid', 'created_at', 'kisalink', 'olusturan', 'thumbnail')


class HotContentSerializer(serializers.ModelSerializer):

    hot = serializers.SerializerMethodField('hotmu')

    def hotmu(self, obj):

        try:
            blog_object = Content.objects.get(id=obj.id)

            time_threshold = blog_object.created_at + datetime.timedelta(hours=24)

            now = datetime.datetime.now().replace(tzinfo=utc)

            if (time_threshold > now):
                if blog_object.goruntulenme > 999:
                    return "true"
                else:
                    return "false"
            else:
                return "false"

        except:
            return "hata"

    class Meta:
        model = Content
        fields = ('id', 'title', 'yayinda', 'hot', 'ozet', 'olusturanid',
                  'created_at', 'kisalink', 'olusturan', 'thumbnail')


class TrendContentSerializer(serializers.ModelSerializer):

    trend = serializers.SerializerMethodField('trendmi')

    def trendmi(self, obj):
        try:
            if ContentComment.objects.filter(post=obj.id).exists():
                blog_comments = ContentComment.objects.filter(post=obj.id)
                if blog_comments.count() > 3:
                    return "true"
                else:
                    return "false"
            else:
                return "false"
        except:
            return "hata"

    class Meta:
        model = Content
        fields = ('id', 'title', 'yayinda', 'trend', 'ozet', 'olusturanid',
                  'created_at', 'kisalink', 'olusturan', 'thumbnail')


class GrupIcerikleriSerializer(serializers.ModelSerializer):
    begenenler = serializers.SlugRelatedField(queryset=GrupIcerikleri.objects.all(), many=True, slug_field="username")
    begendinmi = serializers.SerializerMethodField('begenicheck')
    hashtags = serializers.SerializerMethodField('taggenerator')

    def taggenerator(self, obj):
        blog_object = GrupIcerikleri.objects.get(id=obj.id)
        userx = User.objects.get(username=blog_object.yazan)
        icerikler = blog_object.icerik
        step_0 = re.findall(r"#(\w+)", icerikler)

        blog_object.hashtags = step_0

        for ste in step_0:
            if not Hashtags.objects.filter(tag=ste, author=userx, grup_content=blog_object).exists():
                tago = Hashtags.objects.create(tag=ste, author=userx)
                tago.grup_content.add(blog_object)
                tago.save()
            else:
                return""
        blog_object.save()
        return step_0

    def begenicheck(self, obj):
        request = self.context.get('request', None)
        if obj.begenenler.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def validate(self, attrs):
        yazan = attrs.get('yazan', '')
        grup = attrs.get('grup', '')
        uyeler = grup.uyelerasil.all()
        request = self.context.get('request', None)
        currentus = request.user

        if yazan != currentus:
            raise serializers.ValidationError(
                {'yazan', ('Başkası adına içerik üretemezsin')})

        gruplink = grup.name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace(
            "İ", "i") \
            .replace("ö", "o").replace("ç", "c").replace(" ", "-").replace(".", "")
        notificat = Notification.objects.create(title="'{}' grubunda bir içerik paylaştı.".format(grup.name),
                                                description="/g/{}".format(gruplink))
        notificat.actor.add(currentus.id)

        for uye in uyeler:
            if not uye.id == currentus.id:
                notificat.user.add(uye.id)
                notificat.save()

        return super().validate(attrs)

    def post(self, validated_data):
        request = self.context.get('request', None)
        me = request.user
        return GrupIcerikleri.objects.create(**validated_data)

    class Meta:
        model = GrupIcerikleri
        fields = ('id', 'grup', 'icerik', 'yazan','hashtags', 'begenenler', 'date_added', 'begendinmi', 'image_url', 'date_added')


class GroupSerializer(serializers.ModelSerializer):
    uyeler = serializers.SlugRelatedField(queryset=Group.objects.all(), many=True, slug_field="username")
    uyelerasil = serializers.SlugRelatedField(queryset=Group.objects.all(), many=True, slug_field="username")
    yoneticiler = serializers.SlugRelatedField(queryset=Group.objects.all(), many=True, slug_field="username")
    uyesin = serializers.SerializerMethodField('uyecheck')
    basvurdun = serializers.SerializerMethodField('basvcheck')
    yoneticisin = serializers.SerializerMethodField('yoneticicheck')
    uyesayisi = serializers.SerializerMethodField('uyesay')
    slug = serializers.SerializerMethodField('sluggen')

    def sluggen(self, obj):
        request = self.context.get('request', None)
        return obj.name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("İ",
                                                                                                                "i") \
            .replace("ö", "o").replace("ç", "c").replace(" ", "-").replace(".", "")

    def uyecheck(self, obj):
        request = self.context.get('request', None)
        if obj.uyelerasil.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def basvcheck(self, obj):
        request = self.context.get('request', None)
        if obj.uyeler.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def yoneticicheck(self, obj):
        request = self.context.get('request', None)
        if obj.yoneticiler.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def uyesay(self, obj):
        request = self.context.get('request', None)
        return obj.uyelerasil.count()

    class Meta:
        model = Group
        fields = (
        'id', 'slug', 'puan', 'image_url', 'bilgilendirme', 'olusturulma', 'basvurdun', 'uyelerasil', 'uyesayisi',
        'yoneticisin', 'name', 'description', 'uyeler', 'gizligrup', 'yoneticiler', 'uyesin')


class BlogPostSerializer(serializers.ModelSerializer):
    likes = serializers.SlugRelatedField(queryset=BlogPost.objects.all(), many=True, slug_field="username")
    begeniyorsun = serializers.SerializerMethodField('begenicheck')
    hashtags = serializers.SerializerMethodField('taggenerator')
    tagler = serializers.SerializerMethodField('taglerimiz')
    like_count = serializers.SerializerMethodField('like_counter')

    def taggenerator(self, obj):
        blog_object = BlogPost.objects.get(id=obj.id)
        userx = User.objects.get(username=blog_object.olusturan)
        icerikler = blog_object.icerik
        step_0 = re.findall(r"#(\w+)", icerikler)

        blog_object.hashtags = step_0

        for ste in step_0:
            if not Hashtags.objects.filter(tag=ste, author=userx, blog_content=blog_object).exists():
                tago = Hashtags.objects.create(tag=ste, author=userx)
                tago.blog_content.add(blog_object)
                tago.save()
            else:
                return""
        blog_object.save()
        return step_0

    def taglerimiz(self, obj):
        blog_object = BlogPost.objects.get(id=obj.id)
        body = blog_object.icerik

        hashtag_list = []

        for word in body.split():
            if word[0] == '#':
                hashtag_list.append(word[1:])

        return hashtag_list

    def begenicheck(self, obj):
        request = self.context.get('request', None)
        if obj.likes.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def like_counter(self, obj):
        return obj.likes.count()

    def validate(self, attrs):
        olusturan = attrs.get('olusturan', '')
        request = self.context.get('request', None)
        currentus = request.user.username
        if olusturan != currentus:
            raise serializers.ValidationError(
                {'olusturan', ('Başkası adına içerik üretemezsin')})

        return super().validate(attrs)

    def post(self, validated_data):
        return BlogPost.objects.create(**validated_data)


    class Meta:
        model = BlogPost
        fields = ('id', 'icerik', 'olusturan', 'tarih', 'gorsel', 'likes', 'begeniyorsun', 'hashtags', 'tagler', 'like_count')


class UserListesiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'title', 'description', 'timestamp', 'actor', 'badge', 'badge_img', 'puan_badge',
                  'description_badge', 'seen')


class BadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = ('id', 'adi', 'detay', 'gorseli', 'uyeler', 'puan')


class HashtagsSerializer(serializers.ModelSerializer):

    paylasim = serializers.SerializerMethodField('paylasimhesapla')

    def paylasimhesapla(self, obj):
        tag = Hashtags.objects.filter(tag=obj.tag)
        return tag.count()

    class Meta:
        model = Hashtags
        fields = ('id', 'tag', 'author', 'timestamp', 'content', 'grup_content', 'blog_content', 'comment', 'blog_comment','paylasim')


class ProfileSerializer(serializers.ModelSerializer):
    kullaniciadi = serializers.CharField(source='user.username', read_only=True)
    followers = serializers.SlugRelatedField(queryset=Profile.objects.all(), many=True, slug_field="username")
    takipettiklerim = serializers.SlugRelatedField(queryset=Profile.objects.all(), many=True, slug_field="username")
    takipediyorsun = serializers.SerializerMethodField('takipcheck')
    puan = serializers.SerializerMethodField('puanhesapla')
    rutbe = serializers.SerializerMethodField('rutbehesapla')
    okunma = serializers.SerializerMethodField('readcount')

    def takipcheck(self, obj):
        request = self.context.get('request', None)
        if obj.followers.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def readcount(self, obj):
        request = self.context.get('request', None)
        icerikler = Content.objects.filter(olusturanid=obj.id)
        okunma = 0
        for icerik in icerikler:
            okunma += icerik.goruntulenme
        return okunma

    def puanhesapla(self, obj):
        rutbepuani = obj.points
        for rozet in obj.rozetler.all():
            rutbepuani = rutbepuani + rozet.puan
        return rutbepuani

    def rutbehesapla(self, obj):
        hampuan = obj.points
        for rozet in obj.rozetler.all():
            hampuan = hampuan + rozet.puan
        if ((hampuan > 0) and (hampuan < 999)):
            return "Yeni Üye"
        elif ((hampuan > 999) and (hampuan < 2999)):
            return "Acemi Üye"
        elif ((hampuan > 2999) and (hampuan < 4999)):
            return "İstikrarlı Üye"
        elif ((hampuan > 6999) and (hampuan < 7999)):
            return "Deneyimli Üye"
        elif ((hampuan > 7999) and (hampuan < 9999)):
            return "Onursal Üye"
        elif ((hampuan > 9999) and (hampuan < 14999)):
            return "Gümüş Üye"
        elif ((hampuan > 14999) and (hampuan < 19999)):
            return "Altın Üye"
        elif ((hampuan > 19999) and (hampuan < 9999999999999)):
            return "Platin Üye"
        else:
            return "Rütbesiz Üye"

    class Meta:
        model = Profile
        fields = (
        'user', 'kullaniciadi', 'onayli', 'okunma', 'rozetler', 'dailypoints', 'puan', 'rutbe', 'bio', 'eposta', 'verdigimoylar',
        'location', 'begendiklerim', 'sonraoku', 'birth_date', 'photo', 'ad', 'soyad', 'kapak', 'followers',
        'takipettiklerim', 'takipediyorsun')


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)

    class Meta:
        model = User
        fields = ['token', 'username', 'password', 'email']

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email', ('Bu mail adresi mevcut')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ContentCommentSerializer(serializers.ModelSerializer):
    puan = serializers.SerializerMethodField('puanhesap')
    agree = serializers.SerializerMethodField('agreecheck')
    agreecount = serializers.SerializerMethodField('agreecnt')
    disagree = serializers.SerializerMethodField('disagreecheck')
    disagreecount = serializers.SerializerMethodField('disagreecnt')
    hashtags = serializers.SerializerMethodField('taggenerator')

    def taggenerator(self, obj):
        blog_object = ContentComment.objects.get(id=obj.id)
        userx = User.objects.get(id=blog_object.yazanid)
        icerikler = blog_object.body
        step_0 = re.findall(r"#(\w+)", icerikler)
        blog_object.hashtags = step_0
        blog_object.save()

        for ste in step_0:
            if not Hashtags.objects.filter(tag=ste, author=userx, comment=blog_object).exists():
                tago = Hashtags.objects.create(tag=ste, author=userx)
                tago.comment.add(blog_object)
                tago.save()
            else:
                return ""
        blog_object.save()
        return step_0

    def agreecheck(self, obj):
        request = self.context.get('request', None)
        if obj.yukari.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def agreecnt(self, obj):
        count = obj.yukari.count()
        return count

    def disagreecheck(self, obj):
        request = self.context.get('request', None)
        if obj.asagi.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def disagreecnt(self, obj):
        count = obj.asagi.count()
        return count

    def puanhesap(self, obj):
        return ((obj.yukari.count()) - (obj.asagi.count()))

    def validate(self, attrs):
        yazan = attrs.get('yazan', '')
        yazanid = attrs.get('yazanid', '')
        post = attrs.get('post', '')
        request = self.context.get('request', None)
        currentusr = request.user
        currentus = request.user.username
        if yazan != currentus:
            raise serializers.ValidationError(
                {'yazan', ('Başkası adına içerik üretemezsin')})
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        created_documents = ContentComment.objects.filter(
            yazan=yazan, date_added__gte=date_from).count()
        if created_documents > 4:
            raise serializers.ValidationError(
                {created_documents, ('Günlük maksimum yorum sayısına ulaştın.')})

        if not post.olusturanid == yazanid:
            kisalink = post.title.replace(' ', '-').replace('.', '').lower()
            notificat = Notification.objects.create(title="içeriğine yorum yaptı.",
                                                    description="/i/{}".format(kisalink))
            notificat.actor.add(currentusr.id)
            notificat.user.add(post.olusturanid)
            notificat.save()
        return super().validate(attrs)

    def post(self, validated_data):
        return ContentComment.objects.create(**validated_data)

    class Meta:
        model = ContentComment
        fields = ('id', 'post', 'hashtags', 'yazan','agree', 'agreecount', 'disagree','disagreecount', 'yazanid', 'body', 'date_added', 'puan')


class BlogPostCommentSerializer(serializers.ModelSerializer):
    puan = serializers.SerializerMethodField('puanhesap')
    hashtags = serializers.SerializerMethodField('taggenerator')

    def taggenerator(self, obj):
        blog_object = BlogPostComment.objects.get(id=obj.id)
        userx = User.objects.get(username=blog_object.yazan)
        icerikler = blog_object.body
        step_0 = re.findall("#([a-zA-Z0-9_]{1,50})", icerikler)
        blog_object.hashtags = step_0

        for ste in step_0:
            if not Hashtags.objects.filter(tag=ste, author=userx, blog_comment=blog_object).exists():
                tago = Hashtags.objects.create(tag=ste, author=userx)
                tago.blog_comment.add(blog_object)
                tago.save()
            else:
                return""
        blog_object.save()
        return step_0

    def puanhesap(self, obj):
        return ((obj.yukari.count()) - (obj.asagi.count()))

    def validate(self, attrs):
        yazan = attrs.get('yazan', '')
        blogpost = attrs.get('blogpost', '')
        request = self.context.get('request', None)
        usid = User.objects.get(username=blogpost.olusturan)
        currentus = request.user.username
        if yazan != currentus:
            raise serializers.ValidationError(
                {'yazan', ('Başkası adına içerik üretemezsin')})

        if not usid.id == request.user.id:
            notificat = Notification.objects.create(title="paylaşımına yorum yaptı",
                                                    description="/u/{}".format(blogpost.olusturan))
            notificat.user.add(usid)
            notificat.actor.add(request.user.id)
        return super().validate(attrs)

    def post(self, validated_data):
        return BlogPostComment.objects.create(**validated_data)

    class Meta:
        model = BlogPostComment
        fields = ('id', 'blogpost','hashtags', 'yazan', 'body', 'date_added', 'puan')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class GrupIcerikleriCommentSerializer(serializers.ModelSerializer):
    yukarimi = serializers.SerializerMethodField('yukaricheck')
    asagimi = serializers.SerializerMethodField('asagicheck')

    yukaricnt = serializers.SerializerMethodField('yukaricntcheck')
    asagicnt = serializers.SerializerMethodField('asagicntcheck')

    def yukaricheck(self, obj):
        request = self.context.get('request', None)
        if obj.yukari.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def asagicheck(self, obj):
        request = self.context.get('request', None)
        if obj.asagi.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def yukaricntcheck(self, obj):
        return obj.yukari.count()

    def asagicntcheck(self, obj):
        return obj.asagi.count()

    def validate(self, attrs):
        yazan = attrs.get('yazan', '')
        request = self.context.get('request', None)
        currentus = request.user

        if yazan != currentus:
            raise serializers.ValidationError(
                {'yazan', ('Başkası adına içerik üretemezsin')})
        else:
            blogcontent = attrs.get('blogpost', '')
            grup = blogcontent.grup

            kisaurl = grup.name.lower().replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace(
                "İ", "i") \
                .replace("ö", "o").replace("ç", "c").replace(" ", "-").replace(".", "")

            if grup.uyelerasil.filter(username=request.user.username).exists():

                if blogcontent.yazan != currentus:
                    notificat = Notification.objects.create(title="paylaşımına yorum yaptı",
                                                            description="/g/{}".format(kisaurl))
                    notificat.user.add(blogcontent.yazan)
                    notificat.actor.add(request.user.id)

                return super().validate(attrs)
            else:
                return ""

    def post(self, validated_data):
        return GrupIcerikleriComment.objects.create(**validated_data)

    class Meta:
        model = GrupIcerikleriComment
        fields = (
        'id', 'blogpost', 'yazan', 'body', 'date_added', 'yukaricnt', 'yukari', 'asagi', 'asagicnt', 'yukarimi',
        'asagimi')


class PersonalityResultSerializer(serializers.ModelSerializer):
    related_content = serializers.SerializerMethodField('personality_content')

    def personality_content(self, obj):
        answers = PersonalityAnswer.objects.filter(result=obj.id)
        if answers.count() > 0:
            first_answ = answers[0].id
            qst = PersonalityQuestion.objects.filter(answer=first_answ).last()
            cntt = Content.objects.filter(test=qst.id)
            if cntt.count() > 0:
                return cntt[0].id

    class Meta:
        model = PersonalityResult
        fields = ('id', 'sonuc', 'descr', 'img', 'related_content')


class PersonalityQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalityQuestion
        fields = ('id', 'body', 'olusturan', 'title', 'img', 'answer')


class PersonalityAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalityAnswer
        fields = ('id', 'body', 'result', 'img')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'body', 'olusturan', 'img', 'answer')


class QuizAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswers
        fields = ('id', 'body', 'img', 'dogrumu')


class PollQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = ('id', 'question', 'body', 'olusturan', 'img', 'answer')


class PollAnswerSerializer(serializers.ModelSerializer):
    katilansayisi = serializers.SerializerMethodField('counter')
    katilanyuzdesi = serializers.SerializerMethodField('yuzdehesaplama')
    katildimmi = serializers.SerializerMethodField('katilimcheck')

    def katilimcheck(self, obj):
        request = self.context.get('request', None)
        currentus = request.user
        if obj.katilanlar.filter(id=request.user.id).exists():
            return "true"
        else:
            return "false"

    def counter(self, obj):
        poll_object = PollAnswer.objects.get(id=obj.id)
        gizli = poll_object.katilanlar.count()
        acik = poll_object.katilanlarsecret.count()
        return gizli + acik


    def yuzdehesaplama(self, obj):

       try:
           toplam = 0

           question = PollQuestion.objects.get(answer=obj.id)
           other_answers = question.answer.all()

           for x in other_answers:
               answer = PollAnswer.objects.get(id=x.id)
               gizli = answer.katilanlar.count()
               acik = answer.katilanlarsecret.count()
               katilanlar = gizli + acik
               toplam += katilanlar

           poll_object = PollAnswer.objects.get(id=obj.id)
           gizli = poll_object.katilanlar.count()
           acik = poll_object.katilanlarsecret.count()
           answer_katilanlar = gizli + acik

           if toplam > 0:
               yuzdehesabi_bf = answer_katilanlar / toplam
               yuzdehesabi = yuzdehesabi_bf * 100
               return yuzdehesabi
           else:
               return 0

       except:
           return ""




    class Meta:
        model = PollAnswer
        fields = ('id', 'body', 'img', 'katilanlarsecret', 'katilanlar', 'katilansayisi', 'katilanyuzdesi', 'katildimmi')


class PopulerProfilesSerializer(serializers.ModelSerializer):
    kullaniciadi = serializers.CharField(source='user.username', read_only=True)
    followers = serializers.SlugRelatedField(queryset=Profile.objects.all(), many=True, slug_field="username")
    takipettiklerim = serializers.SlugRelatedField(queryset=Profile.objects.all(), many=True, slug_field="username")
    takipediyorsun = serializers.SerializerMethodField('takipcheck')
    puan = serializers.SerializerMethodField('puanhesapla')
    rutbe = serializers.SerializerMethodField('rutbehesapla')

    def takipcheck(self, obj):
        request = self.context.get('request', None)
        if obj.followers.filter(username=request.user.username).exists():
            return "true"
        else:
            return "false"

    def puanhesapla(self, obj):
        rutbepuani = obj.points
        for rozet in obj.rozetler.all():
            rutbepuani = rutbepuani + rozet.puan
        return rutbepuani

    def rutbehesapla(self, obj):
        hampuan = obj.points
        for rozet in obj.rozetler.all():
            hampuan = hampuan + rozet.puan
        if ((hampuan > 0) and (hampuan < 999)):
            return "Yeni Üye"
        elif ((hampuan > 999) and (hampuan < 2999)):
            return "Acemi Üye"
        elif ((hampuan > 2999) and (hampuan < 4999)):
            return "İstikrarlı Üye"
        elif ((hampuan > 6999) and (hampuan < 7999)):
            return "Deneyimli Üye"
        elif ((hampuan > 7999) and (hampuan < 9999)):
            return "Onursal Üye"
        elif ((hampuan > 9999) and (hampuan < 14999)):
            return "Gümüş Üye"
        elif ((hampuan > 14999) and (hampuan < 19999)):
            return "Altın Üye"
        elif ((hampuan > 19999) and (hampuan < 9999999999999)):
            return "Platin Üye"
        else:
            return "Rütbesiz Üye"

    class Meta:
        model = Profile
        ordering = ['dailypoints']
        fields = (
        'user', 'dailypoints', 'kullaniciadi', 'onayli', 'rozetler', 'puan', 'rutbe', 'bio', 'eposta', 'verdigimoylar',
        'location', 'begendiklerim', 'sonraoku', 'birth_date', 'photo', 'ad', 'soyad', 'kapak', 'followers',
        'takipettiklerim', 'takipediyorsun')


class ConversationSerializer(serializers.ModelSerializer):

    userone_ka = serializers.SerializerMethodField('useroneka')
    usertwo_ka = serializers.SerializerMethodField('usertwoka')
    other_user = serializers.SerializerMethodField('otherka')
    other_userid = serializers.SerializerMethodField('otherid')
    last_msg = serializers.SerializerMethodField('last_get')
    msg_count = serializers.SerializerMethodField('count_get')
    last_sndr = serializers.SerializerMethodField('lastsender_get')
    msg_timestamp = serializers.SerializerMethodField('last_timestamp')
    accepted = serializers.SerializerMethodField('check_accepted')
    u_deleted = serializers.SerializerMethodField('check_deleted')

    def useroneka(self, obj):
        kullaniciadi = User.objects.get(id=obj.user_one.id)
        return kullaniciadi.username

    def check_deleted(self, obj):
        request = self.context.get('request', None)
        me = request.user
        if obj.deleted_by.filter(pk=me.id).exists():
            return "true"
        else:
            return "false"

    def usertwoka(self, obj):
        kullaniciadi = User.objects.get(id=obj.user_two.id)
        return kullaniciadi.username

    def check_accepted(self, obj):
        request = self.context.get('request', None)
        me = request.user
        if obj.created_users.filter(pk=me.id).exists():
            return "true"
        else:
            return "false"

    def otherka(self, obj):
        request = self.context.get('request', None)
        me = request.user

        if me.id==obj.user_one.id:
            kullaniciadi = User.objects.get(id=obj.user_two.id)
            return kullaniciadi.username
        if me.id==obj.user_two.id:
            kullaniciadi = User.objects.get(id=obj.user_one.id)
            return kullaniciadi.username

    def otherid(self, obj):
        request = self.context.get('request', None)
        me = request.user

        if me.id==obj.user_one.id:
            kullaniciadi = User.objects.get(id=obj.user_two.id)
            return kullaniciadi.id
        if me.id==obj.user_two.id:
            kullaniciadi = User.objects.get(id=obj.user_one.id)
            return kullaniciadi.id

    def last_get(self, obj):
        request = self.context.get('request', None)
        me = request.user
        try:
            last_message = Messages.objects.filter(conversation_key=obj.id, owner=me).latest('timestamp')
            return last_message.msg_content
        except:
            return ""

    def count_get(self, obj):
        msg = Messages.objects.filter(conversation_key=obj.id)
        return msg.count()


    def lastsender_get(self, obj):
        try:
            last_message = Messages.objects.filter(conversation_key=obj.id).latest('timestamp')
            return last_message.sender.username
        except:
            return ""

    def last_timestamp(self, obj):
        request = self.context.get('request', None)
        me = request.user
        try:
            last_message = Messages.objects.filter(conversation_key=obj.id, owner=me).latest('timestamp')

            now = datetime.datetime.now().replace(tzinfo=utc).strftime('%Y-%m-%d')
            tarih = last_message.timestamp.replace(tzinfo=utc).strftime('%Y-%m-%d')
            yesterdayx = datetime.datetime.now() - datetime.timedelta(1)
            yesterday = yesterdayx.strftime('%Y-%m-%d')

            if tarih == now:
                saat = last_message.timestamp.strftime('%H:%M')
                return saat
            elif tarih == yesterday:
                saat = last_message.timestamp.strftime('%H:%M')
                return "Dün - {}".format(saat)
            else:
                saat = last_message.timestamp.strftime('%H:%M')
                return "tarih - {}".format(saat)
        except:
            return ""

    class Meta:
        model = Conversation
        fields = ('id', 'accepted', 'u_deleted', 'user_one', 'user_two', 'userone_ka', 'usertwo_ka', 'created_users','other_user', 'other_userid', 'last_msg', 'msg_count','last_sndr', 'msg_timestamp')


class MessagesSerializer(serializers.ModelSerializer):
    sender_un = serializers.SerializerMethodField('senderun')
    reciever_un = serializers.SerializerMethodField('receiverun')
    gonderim_zamani = serializers.SerializerMethodField('get_zaman')

    def senderun(self, obj):
        kullaniciadi = User.objects.get(id=obj.sender.id)
        return kullaniciadi.username

    def receiverun(self, obj):
        kullaniciadi = User.objects.get(id=obj.reciever.id)
        return kullaniciadi.username

    def get_zaman(self, obj):
        now = datetime.datetime.now().replace(tzinfo=utc).strftime('%Y-%m-%d')
        tarih = obj.timestamp.replace(tzinfo=utc).strftime('%Y-%m-%d')
        yesterdayx = datetime.datetime.now() - datetime.timedelta(1)
        yesterday = yesterdayx.strftime('%Y-%m-%d')

        if tarih == now:
            saat = obj.timestamp.strftime('%H:%M')
            return saat
        elif tarih == yesterday:
            saat = obj.timestamp.strftime('%H:%M')
            return "Dün - {}".format(saat)
        else:
            saat = obj.timestamp.strftime('%H:%M')
            return "tarih - {}".format(saat)

    class Meta:
        model = Messages
        ordering = ['-id']
        fields = ('id', 'sender', 'sender_un', 'reciever', 'reciever_un', 'conversation_key', 'msg_content', 'timestamp', 'gonderim_zamani', 'seen')


class HelpMessagesSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        sender = attrs.get('sender', '')

        request = self.context.get('request', None)
        currentuser = request.user

        if sender != currentuser:
            raise serializers.ValidationError(
                {'sender', ('Başkası adına içerik üretemezsin')})

        return super().validate(attrs)

    def post(self, validated_data):
        request = self.context.get('request', None)
        return HelpMessages.objects.create(**validated_data)

    class Meta:
        model = HelpMessages
        fields = ('id', 'sender', 'body', 'date_added', 'replied')
