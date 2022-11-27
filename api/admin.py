from django.contrib import admin
from .models import Content, GrupIcerikleriComment, PersonalityResult, PersonalityQuestion, PersonalityAnswer, Quiz, \
    QuizAnswers, PollQuestion, PollAnswer, Badges, Conversation, Messages, Hashtags
from .models import Profile
from .models import BlogPost
from .models import BlogPostComment
from .models import ContentComment
from .models import Group
from .models import GrupIcerikleri
from .models import Notification
from .models import HelpMessages


# Register your models here.


admin.site.register(Content)
admin.site.register(Profile)
admin.site.register(Conversation)
admin.site.register(Messages)
admin.site.register(HelpMessages)
admin.site.register(Hashtags)
admin.site.register(Notification)
admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
admin.site.register(ContentComment)
admin.site.register(Group)
admin.site.register(GrupIcerikleri)
admin.site.register(GrupIcerikleriComment)
admin.site.register(PersonalityResult)
admin.site.register(PersonalityQuestion)
admin.site.register(PersonalityAnswer)
admin.site.register(Quiz)
admin.site.register(QuizAnswers)
admin.site.register(PollQuestion)
admin.site.register(PollAnswer)
admin.site.register(Badges)

