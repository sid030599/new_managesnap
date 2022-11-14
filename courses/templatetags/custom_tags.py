from django import template
from courses.models import myAssignment, myCourseUnit, mytopics

register = template.Library()

@register.filter(name='get_percentage')
def get_percentage(course, user):
    # topic = courseTopic.objects.filter
    
    regular_units = myCourseUnit.objects.filter(user__id=user, courseunit__course__id=course).exclude(courseunit__name='Unit Lessons')

    total_topic = 0

    for unit in regular_units:
        total_topic += unit.coursetopics.all().count()

    total_assignment = myAssignment.objects.filter(assignment__course__id=course, user__id=user).count()
    unit_lesson = myCourseUnit.objects.get(user__id=user, courseunit__course__id=course, courseunit__name='Unit Lessons')

    total_unit_topics = 0
        

    done_topic = mytopics.objects.filter(coursetopic__course__id=course, done=True, user__id=user).exclude(coursetopic__title='Unit Lessons').count()
    done_assignment = myAssignment.objects.filter(assignment__course__id=course, user__id=user, done=True).count()

    done_unit_topics = 0

    for topic in unit_lesson.coursetopics.all():
        total_unit_topics += topic.documents.all().count()
        done_unit_topics += topic.documents.filter(done=True).count()



    done = done_topic + done_assignment + done_unit_topics
    total = total_assignment + total_topic + total_unit_topics
    if done==0:
        return 0;
    percentage = done / total
    return round(percentage*100, 2)



@register.filter(name='unit_status')
def unit_status(mytopicid , documentid):
    
    my_topic = mytopics.objects.get(id=mytopicid)
    documents = my_topic.documents
    done = documents.get(document__id=documentid).done

    print(done)

    return done
