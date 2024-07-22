from rest_framework import serializers
from .models import (
    Category,
    Quiz,
    Question,
    Option,
    ResultOfQuiz
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'quiz_count'
        )


class QuizSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = (
            'id',
            'title',
            'category',
            'question_count'
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'id',
            'option_text',
            'is_right'
        )


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True) #optionkey'ini modelde tanımladığımız related_name'den görüyor yoksa option__set ile görebilir.
    quiz = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = (
            'id',
            'quiz',
            'title',
            'options',
            'difficulty'
        )

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultOfQuiz
        fields = (
            'id',
            'name',
            'correct',
            'wrong',
            'emty',
            'score',
            'status'
        )
# title = models.TextField()
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     difficulty = models.CharField(max_length=1, choices=SCALE)
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'name', 'description', 'url', 'image']
        read_only_fields = ['url']

# from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True,required=False)  # Dosya yüklemeleri için

    class Meta:
        model = Photo
        fields = ['id', 'name', 'description', 'url', 'image']
        read_only_fields = ['url']        