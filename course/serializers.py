from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from course.models import Course, Lesson, Subscription
from course.validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    validators = [YouTubeValidator(field="link")]
    fields = '__all__'

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_subscription(self, instance):
        user = self.context['request'].user
        return Subscription.objects.all().filter(user=user).filter(course=instance).exists()


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lessons", many=True)

    def get_lesson_count(self, obj):
        return obj.lessons.all().count()

    class Meta:
        model = Course
        fields = ("lesson_count", "lesson", "title", "description")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("is_subscribed",)
