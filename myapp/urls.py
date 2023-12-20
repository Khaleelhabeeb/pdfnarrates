from django.urls import path
from .views import index, home, upload, pdf_upload, download_docx, image_to_pdf, words_to_pdf

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('upload/', upload, name='upload'),
    path('pdf_upload/', pdf_upload, name='pdf_upload'),
    path('download_docx/', download_docx, name='download_docx'),
    path('image_to_pdf/', image_to_pdf, name='image_to_pdf'),
    path('words_to_pdf', words_to_pdf, name='word_to_pdf'),
]

