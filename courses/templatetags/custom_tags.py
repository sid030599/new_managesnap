from django import template
from courses.models import myAssignment, myCourseUnit, mytopics,Unit,course, Lesson, LessonFile,MyUnit,MyLesson

register = template.Library()

@register.filter(name='get_percentage')
def get_percentage(courseid, user):

    myunits = MyUnit.objects.filter(course__id = courseid)
    totalunits = MyUnit.objects.filter(course__id = courseid).count()
    total_per = 0
    for i in myunits:
        total_per +=(get_unit_percentage(i.id,user)/totalunits)
    # topic = courseTopic.objects.filter
    
    # regular_units = myCourseUnit.objects.filter(user__id=user, courseunit__course__id=courseid).exclude(courseunit__name='Unit Lessons')

    # total_topic = 0

    # for unit in regular_units:
    #     total_topic += unit.coursetopics.all().count()

    # total_assignment = myAssignment.objects.filter(assignment__course__id=courseid, user__id=user).count()
    
    # if Unit.objects.filter(course=courseid).exists():
    #     unit_lesson = Unit.objects.filter(course__id=courseid).first()
    #     lesson = Lesson.objects.filter(unit = unit_lesson)

    # total_unit_topics = 0
        

    # done_topic = mytopics.objects.filter(coursetopic__course__id=courseid, done=True, user__id=user).exclude(coursetopic__title='Unit Lessons').count()
    # done_assignment = myAssignment.objects.filter(assignment__course__id=courseid, user__id=user, done=True).count()

    # done_unit_topics = 0

    # # for topic in unit_lesson.coursetopics.all():
    # #     total_unit_topics += topic.documents.all().count()
    # #     done_unit_topics += topic.documents.filter(done=True).count()



    # #done = done_topic + done_assignment + done_unit_topics
    # done =  done_assignment 

    # total = total_assignment 
    # #total = total_assignment + total_topic + total_unit_topics
    # if done==0:
    #     return 0;
    
    return total_per

@register.filter(name='get_unit_percentage')
def get_unit_percentage(unitid,user):
    # topic = courseTopic.objects.filter
    
    unit = MyUnit.objects.get(id = unitid)
    #print(unit)
    all_lesson = MyLesson.objects.filter(unit__id = unit.unit.id).count()
    #print(all_lesson,'all')
    lesson_comp = MyLesson.objects.filter(unit__id = unit.unit.id,user__id = user,isdone = True).count()
    #print(lesson_comp)
    if all_lesson != 0:

        percentage = lesson_comp / all_lesson
    
        return round(percentage*100, 2)


@register.filter(name='unit_status')
def unit_status(mytopicid , documentid):
    
    my_topic = mytopics.objects.get(id=mytopicid)
    documents = my_topic.documents
    done = documents.get(document__id=documentid).done

    #print(done)

    return done
