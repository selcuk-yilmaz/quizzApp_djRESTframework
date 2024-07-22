from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import (
    Category,
    Quiz,
    Question,
    Option,
    ResultOfQuiz
)
from .serializers import (
    CategorySerializer,
    QuizSerializer,
    QuestionSerializer,
    ResultSerializer
)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class QuizList(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']    

class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['quiz', 'difficulty']    


class ResultsGetPost(ModelViewSet):
    queryset=ResultOfQuiz.objects.all()
    serializer_class=ResultSerializer    



from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
import cloudinary.uploader
from rest_framework.parsers import MultiPartParser, FormParser

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)  # Dosya ve form verilerini işlemek için parser sınıfları

    def create(self, request, *args, **kwargs):
        # Yüklenen dosyayı al
        if 'image' not in request.FILES:
            return Response({"image": ["No file was submitted."]}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['image']

        # Dosyayı Cloudinary'ye yükle
        try:
            upload_result = cloudinary.uploader.upload(file, folder="quizApp_DRF", use_filename=True)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Photo modelini oluşturmak için gerekli verileri topla
        photo_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'url': upload_result['secure_url'],
            'image_id': upload_result['public_id']
        }

        # Serializer ile veriyi doğrula ve kaydet
        serializer = self.get_serializer(data=photo_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import cloudinary.uploader
from .models import Photo
from .serializers import PhotoSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Cloudinary'ye yükle
        upload_result = cloudinary.uploader.upload(
            serializer.validated_data['image'],
            folder="english_quiz",
            use_filename=True
        )

        # print("yüklenen resim",upload_result)
        # Modeli kaydet
        photo = Photo.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            url=upload_result['secure_url'],
            # image_id=upload_result['public_id']
        )
        
        return Response(PhotoSerializer(photo).data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
