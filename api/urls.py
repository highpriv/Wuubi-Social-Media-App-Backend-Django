from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import current_user, UserList, AllUsersViewSet, GroupViewSet, updategroup, profile_detail_view, \
    ContentViewSet, \
    ProfileViewSet, yoneticieklekaldir, user_follow_view, begeniyeekle, contentcomment_up, grupislemleri, blogpost_like, \
    BlogPostViewSet, ContentCommentViewSet, BlogPostCommentViewSet, blogcomment_up, ChangePasswordView, sonraokuyaekle, \
    GrupIcerikleriViewSet, emoji_ver, BadgesViewSet, grcontentbegen, GrupIcerikleriCommentViewSet, \
    set_conversation_seen, \
    grupcomment_up, \
    uyekabulred, \
    uyekaldir, \
    PersonalityResultViewSet, PersonalityQuestionViewSet, PersonalityAnswerViewSet, testgetir, testhesapla, \
    QuizQuestionViewSet, QuizAnswerViewSet, testgetirq, PollAnswerViewSet, PollQuestionViewSet, polloyver, \
    PopulerProfilesViewSet, HelpMessagesViewSet, notificationcheck, setallseen, NotificationViewSet, \
    ConversationViewSet, MessagesViewSet, \
    delete_conversation, HashtagsViewSet, blogpost_sil, blogpost_edit, content_edit, test_question_edit, \
    test_answer_edit, ContentMinimalViewSet, PopularContentViewSet, HotContentViewSet, TrendContentViewSet, \
    check_new_msg, deleteuser

from . import views

router = routers.DefaultRouter()
router.register('contents', ContentViewSet)
router.register('test-result', PersonalityResultViewSet)
router.register('test-question', PersonalityQuestionViewSet)
router.register('test-answer', PersonalityAnswerViewSet)
router.register('get-conversations', ConversationViewSet, basename='Conversations')
router.register('get-messages', MessagesViewSet, basename='Messages')
router.register('get-notifications', NotificationViewSet, basename='Notifications')
router.register('quiz-question', QuizQuestionViewSet)
router.register('quiz-answer', QuizAnswerViewSet)
router.register('poll-question', PollQuestionViewSet)
router.register('poll-answer', PollAnswerViewSet)
router.register('grcontents', GrupIcerikleriViewSet, basename='GroupIcerikleris')
router.register('gruplar', GroupViewSet, basename='Groups')
router.register('profile', ProfileViewSet)
router.register('badges', BadgesViewSet, basename='Badges')
router.register('blogpost', BlogPostViewSet)
router.register('blogpostcomment', BlogPostCommentViewSet)
router.register('grupicerigicomment', GrupIcerikleriCommentViewSet)
router.register('hashtags', HashtagsViewSet)
router.register('contentcomment', ContentCommentViewSet)
router.register('minimal-contents', ContentMinimalViewSet)
router.register('popular-contents', PopularContentViewSet)
router.register('hot-contents', HotContentViewSet)
router.register('trend-contents', TrendContentViewSet)
router.register('help-desk', HelpMessagesViewSet)
router.register('populeruyeler', PopulerProfilesViewSet)
router.register('butunuyeler', AllUsersViewSet, basename='AllUsers')

urlpatterns = [
    path('', include(router.urls)),
    path('current_user/', current_user),
    path('notificationcheck/', notificationcheck),
    path('setallseen/', setallseen),
    path('test-hesapla/', testhesapla),
    path('<str:username>', profile_detail_view),
    path('<str:username>/follow', user_follow_view),
    path('<str:id>/begeni', blogpost_like),
    path('<str:id>/test-question-edit', test_question_edit),
    path('<str:id>/test-answer-edit', test_answer_edit),
    path('<str:id>/katil', grupislemleri),
    path('<str:id>/delete-conversation', delete_conversation),
    path('<str:id>/poll-oyver', polloyver),
    path('<str:id>/modedit', yoneticieklekaldir),
    path('<str:id>/content-edit', content_edit),
    path('<str:id>/davetiye', uyekabulred),
    path('<str:id>/test-getir', testgetir),
    path('<str:id>/set-conversation-seen', set_conversation_seen),
    path('check-msg/', check_new_msg),
    path('<str:id>/test-getirq', testgetirq),
    path('<str:id>/gredit', updategroup),
    path('<str:id>/grupusdel', uyekaldir),
    path('<str:id>/cbegeni', begeniyeekle),
    path('<str:id>/grcnbegeni', grcontentbegen),
    path('<str:id>/emoji', emoji_ver),
    path('<str:id>/sonraoku', sonraokuyaekle),
    path('<str:id>/userdelete', deleteuser),
    path('<str:id>/updown', blogcomment_up),
    path('<str:id>/blogpost-sil', blogpost_sil),
    path('<str:id>/blogpost-duzenle', blogpost_edit),
    path('<str:id>/gcupdown', grupcomment_up),
    path('<str:id>/cupdown', contentcomment_up),
    path('fx/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/', UserList.as_view()),

]




