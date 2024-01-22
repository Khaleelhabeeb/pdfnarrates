from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import FileResponse
from .utils import extract_text_from_pdf, convert_pdf_to_docx

import json
from gtts import gTTS
import base64
import io
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from img2pdf import convert

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def upload(request):
    if request.method == "POST":
        if 'pdfFile' not in request.FILES:
            return HttpResponse("No file part")

        pdf_file = request.FILES['pdfFile']

        if pdf_file.name == '':
            return HttpResponse("No selected file")

        # Extract text from the PDF using PyMuPDF (fitz)
        pdf_text = extract_text_from_pdf(pdf_file)

        # Convert text to speech using gTTS
        tts = gTTS(pdf_text, lang='en', tld='us')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Encode audio data in Base64
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

        return render(request, 'result.html', {'audio_data': audio_base64})

    return render(request, "upload.html")


def pdf_upload(request):
    if request.method == "POST":
        if 'pdfFile' not in request.FILES:
            return HttpResponse("No file part")

        pdf_file = request.FILES['pdfFile']

        if pdf_file.name == '':
            return HttpResponse("No selected file")

        
        docx_content = convert_pdf_to_docx(pdf_file)

        if docx_content is None:
            return HttpResponse("Error converting PDF to DOCX")

        # Render docx.html with the content
        return render(request, 'docx.html', {'docx_content': docx_content})

    return render(request, "pdf_upload.html")

def download_docx(request):
    docx_content = request.POST.get("docx_content")

    if docx_content is None:
        return HttpResponse("Error: No DOCX content")

    # Decode the Base64 content
    docx_data = base64.b64decode(docx_content)

    return FileResponse(io.BytesIO(docx_data), as_attachment=True, filename='output.docx')


def image_to_pdf(request):
    if request.method == "POST":
        image_files = request.FILES.getlist('imageFiles')

        if not image_files:
            return HttpResponse("No selected files")

        # Create a BytesIO buffer to store the PDF content
        pdf_buffer = BytesIO()

        # List to store individual image file data
        all_images_data = []

        for image_file in image_files:
            # Append image file data to the list
            all_images_data.append(image_file.read())

        # Convert the list of image file data to a single PDF file
        pdf_data = convert(all_images_data)

        # Write the PDF content to the buffer
        pdf_buffer.write(pdf_data)

        # Reset the buffer's position to the beginning
        pdf_buffer.seek(0)

        # Provide the user with a downloadable link for the PDF file
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=output.pdf'
        return response

    return render(request, "image_to_pdf.html")

def words_to_pdf(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_content = data.get('content', '')

            
            img = Image.new('RGB', (800, 600), color='white')
            d = ImageDraw.Draw(img)

            
            font = ImageFont.load_default()

            
            d.text((10, 10), user_content, font=font, fill='black')

            # Create a BytesIO buffer to store the PDF content
            pdf_buffer = BytesIO()

            # Save the image to the buffer as a PDF
            img.save(pdf_buffer, format='PDF')

            # Reset the buffer's position to the beginning
            pdf_buffer.seek(0)

            # Provide the user with a downloadable link for the PDF file
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=output.pdf'
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    return render(request, "words_to_pdf.html")

def server_error(request):
    return render(request, 'errors/500.html', status=500)

def not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


