from unicodedata import category
from django.db import models


class UpdateCreateDate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):  # Categorys  --> ies
    name = models.CharField(max_length=50, verbose_name='Category Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def quiz_count(self):
        return self.quizz.count()  # bACKEND ---> 15 quiz


class Quiz(UpdateCreateDate):
    title = models.CharField(max_length=50, verbose_name='Quiz title')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='quizz')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quizzes'

    @property
    def question_count(self):
        return self.question_set.count()


class Question(UpdateCreateDate):

    SCALE = (
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced')
    )

    title = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=1, choices=SCALE)

    def __str__(self):
        return f'{self.title} - {self.quiz.category}'


class Option(UpdateCreateDate):
    option_text = models.CharField(max_length=200)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text
    
class  ResultOfQuiz(UpdateCreateDate):
    SCALE = (
        ('poor', 'poor'),
        ('medium', 'medium'),
        ('normal', 'normal'),
        ('good', 'good'),
        ('perfect', 'perfect')
    )
    name = models.CharField(max_length=50, verbose_name='Student Name')
    correct = models.CharField(max_length=30)
    wrong= models.CharField(max_length=15)
    emty = models.CharField(max_length=200)
    score = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=SCALE)

    def __str__(self):
        return self.status

class Photo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=200)
    # image_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name