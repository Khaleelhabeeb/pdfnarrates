from django.test import TestCase
from myapp.utils import extract_text_from_pdf, convert_pdf_to_docx
from myapp.views import index, upload, home, pdf_upload, download_docx, image_to_pdf, words_to_pdf
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

class UtilsTests(TestCase):
    def test_extract_text_from_pdf(self):
        # Assuming you have a sample PDF file for testing
        pdf_path = "path/to/sample.pdf"
        pdf_file = SimpleUploadedFile("sample.pdf", open(pdf_path, "rb").read())

        extracted_text = extract_text_from_pdf(pdf_file)
        self.assertIsNotNone(extracted_text)
        self.assertIsInstance(extracted_text, str)
        self.assertGreater(len(extracted_text), 0)

    def test_convert_pdf_to_docx(self):
        # Assuming you have a sample PDF file for testing
        pdf_path = "path/to/sample.pdf"
        pdf_file = SimpleUploadedFile("sample.pdf", open(pdf_path, "rb").read())

        docx_content = convert_pdf_to_docx(pdf_file)
        self.assertIsNotNone(docx_content)
        self.assertIsInstance(docx_content, str)
        self.assertGreater(len(docx_content), 0)

class ViewsTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_upload_view(self):
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)

        # Assuming you have a sample PDF file for testing
        pdf_path = "path/to/sample.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            response = self.client.post(reverse('upload'), {'pdfFile': pdf_file})
            self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_pdf_upload_view(self):
        response = self.client.get(reverse('pdf_upload'))
        self.assertEqual(response.status_code, 200)

        # Assuming you have a sample PDF file for testing
        pdf_path = "path/to/sample.pdf"
        with open(pdf_path, 'rb') as pdf_file:
            response = self.client.post(reverse('pdf_upload'), {'pdfFile': pdf_file})
            self.assertEqual(response.status_code, 200)

    def test_image_to_pdf_view(self):
        response = self.client.get(reverse('image_to_pdf'))
        self.assertEqual(response.status_code, 200)

        # Assuming you have sample image files for testing
        image_files = ['path/to/image1.jpg', 'path/to/image2.jpg']
        image_file_data = [open(image_path, 'rb') for image_path in image_files]

        response = self.client.post(reverse('image_to_pdf'), {'imageFiles': image_file_data})
        self.assertEqual(response.status_code, 200)

    def test_words_to_pdf_view(self):
        response = self.client.get(reverse('words_to_pdf'))
        self.assertEqual(response.status_code, 200)

        # Assuming you have sample user-typed content for testing
        user_content = 'Lorem Ipsum'
        response = self.client.post(reverse('words_to_pdf'), {'content': user_content})
        self.assertEqual(response.status_code, 200)

