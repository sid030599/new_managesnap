from django.urls import path
import courses.views as views 
import account.views as vi
urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.coursepage, name='course'),
    #payment
    path('success/<int:courseid>', views.success, name='payment_status'),
    path('payment/<int:courseid>', views.payment1, name='make-payment'),

    path('<courseid>/coursedetail/', views.courseDetail, name='courseDetail'),
    path('<courseid>/courseunits/', views.courseunit, name='courseUnits'),
    path('<courseid>/student_learning_page/', views.student_learning_page, name='student_learning_page'),
    path('<courseid>/test-assign-page/', views.test_assign_page, name='test-assign-page'),
    path('lms<courseid>/student-files/', views.student_files, name='student-files'),
    path('assignedetail/<str:obj>/<courseid>', views.assignDetail, name='assignDetail'),
    path('announcedetail/<str:obj>/<courseid>', views.announceDetail, name='announceDetail'),
    path('unitedetail/<str:obj>/<courseid>', views.unitDetail, name='unitDetail'),
    path('signup', vi.handlesignup, name='handlesignup'),
    path('<courseid>/<studentid>/enroll/', views.enrollcourse, name='enroll'),
    path('logout/', vi.handlelogout, name='handlelogout'),
    path('login', vi.handlelogin, name='handlelogin'),
    path('<coursetopic>/topiccomplete/', views.topiComp, name='topic-complete'),
    path('<assignmentid>/assignment_complete/', views.assignmentComp, name='assignment-complete'),
    path('mycourses/', views.usercourse, name='usercourse'),
    path('all_courses/', views.all_courses, name='all-courses'),
    path('create_course', views.create_course, name='create-course'),
    path('create_course_unit', views.create_course_unit, name='create-course-unit'),
    path('create_topic/<str:obj>', views.create_topic, name='create-topic'),
    path('create_unit/<str:obj>', views.create_unit, name='create-unit'),
    path('update_unit/<str:obj>/<int:unitid>', views.update_unit, name='update-unit'),
    path('enroll_students/<courseid>/', views.enrollstudents, name='enroll-students'),
    path('teacher_signup', vi.handleteachersignup, name='teacher-signup'),
    path('groups/', views.groups, name='groups'),
    path('groups_students/<int:pk>', views.group_student, name='group_student'),
    path('student_profile/<int:pk>', views.profile, name='profile'),
    path('create_group', views.create_group, name='create-group'),
    path('group_detail/<groupid>', views.group_detail, name='group-detail'),
    path('add_student/<groupid>/<studentid>/', views.add_student_to_group, name='add-student'),
    path('remove_student/<groupid>/<studentid>/', views.remove_student_to_group, name='remove-student'),
    path('enroll/<courseid>/<groupid>/', views.enroll_group, name='enroll-group'),
    path('topic/<str:obj>/<topicid>/<courseid>', views.topic_detail, name='topic-detail'),
    path('unit/<str:obj>/<unitid>/<courseid>', views.unit_detail, name='unit-detail'),
    path('links/<int:pk>',views.show_links,name = 'show-links'),
    path('document/<str:slug>',views.show_document,name = 'show-documents'),
    path('update/<str:obj>/<int:lessonid>/<int:unitid>/<int:courseid>', views.update_lesson, name='update-lesson'),
    path('delete/<str:obj>/<int:lessonid>/<int:unitid>/<int:courseid>', views.delete_lesson, name='delete-lesson'),
    path('topic/<int:id>/<courseid>', views.stu_topic_detail, name='stu-topic-detail'),
    path('announce/<int:topicid>/<courseid>', views.stu_announce_detail, name='stu-announce-detail'),
    path('lesson_detail/<courseid>/<int:lessonid>',views.lesson_detail,name = 'lesson-detail'),
    path('topic/<str:obj>/<int:topicid>/<courseid>/release', views.release_topic, name='release-topic'),

    path('assignment/<str:obj>/<assignmentid>/<courseid>/release', views.release_assignment, name='release-assignment'),
    path('assignment/<str:obj>/<assignmentid>/<courseid>', views.assignment_detail, name='assignment-detail'),
    path('assignment/<assignmentid>/<courseid>', views.stu_assignment_detail, name='stu-assignment-detail'),
    
    path('submit_assignment', views.submit_assignment, name='submit-assignment'),
    path('topic_delete/<topicid>/<courseid>', views.topic_delete, name='topic-delete'),
    path('assignment_delete/<assignmentid>/<courseid>', views.assignment_delete, name='assignment-delete'),
    #path('all_announcements/', views.all_announcements, name='all-announcements'),
    path('grades', views.grades, name='add-grades'),
    path('unit_topic_complete/<documentid>/', views.unitTopiComp, name='unit-topic-complete'),
    path('unit_complete/<lessonid>/', views.lessonComp, name='unit-complete'),
    path('add_file/<courseid>', views.add_file, name='add-file'),
    path('edit_topic/<courseid>', views.edit_topic, name='edit-topic'),
    path('unenroll_student/<studentid>/<courseid>/', views.unenroll_student, name='unenroll-student'),
    path('submitted/<assignmentid>/', views.submitted, name='submitted'),
    path('not_submitted/<assignmentid>/', views.not_submitted, name='not-submitted'),
    path('graded/<assignmentid>/', views.graded, name='graded'),
    path('not_graded/<assignmentid>/', views.not_graded, name='not-graded'),
    path('search_students/', views.search_students, name='search-students'),
    path('edit_course/', views.edit_course, name='edit-course'),
    path('rename_file/', views.rename_file, name='rename-file'),
    path('delete_file/<obj>/<documentid>/<topicid>/<courseid>', views.delete_file, name='delete-file'),
    path('delete_assignment_file/<documentid>/<assignmentid>/<courseid>', views.delete_assignment_file, name='delete-assignment-file'),
    path('add_link/<courseid>', views.add_link, name='add-link'),
    path('delete_link_assignment/<assignmentid>/<link>/<courseid>', views.delete_link_assignment, name='delete-link-assignment'),
    path('delete_link_topic/<obj>/<topicid>/<str:link>/<courseid>', views.delete_link_topic, name='delete-link-topic'),
    path('topic_stats/<topicid>/', views.topic_stats, name='topic-stats'),
    path('assignment_stats/<assignmentid>/', views.assignment_stats, name='assignment-stats'),
    path('topic_unit_stats/<topicid>/<documentid>/', views.topic_unit_stats, name='topic-unit-stats'),
    path('course_stats/<courseid>/', views.course_stats, name='course-stats'),
    path('my_grades/', views.my_grades, name='my-grades'),
    path('delete_course/<courseid>/', views.delete_course, name='delete-course'),


    path('lms/stud_setting/',views.student_setting,name='stu-setting'),
    path('managesnap/verify_request/<userid>',views.accept_req,name = 'accept_req'),
    path('managesnap/verify_request/<userid>',views.reject_req,name = 'reject_req'),
    path('managesnap/manager_noti/',views.manager_noti,name = 'manager_noti'),
    path('managesnap/manager_event/',views.manager_event,name = 'manager_event'),

    path('managesnap/teacher_profile/',views.teacher_profile,name = 'teacher_profile'),
    path('managesnap/update_noti/<str:obj>/',views.update_man_not,name = 'noti-news'),
    path('managesnap/del_noti/<str:obj>/<int:id>/',views.del_man_not,name = 'del_noti-news'),

]
