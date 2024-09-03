import pdfplumber
from django.http import HttpResponse
from django.shortcuts import render
from .forms import PDFUploadForm

def pdf_to_csv_view(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']

            # CSV faylni yaratish
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="output.csv"'

            # PDF faylni ochish
            with pdfplumber.open(pdf_file) as pdf:
                # Har bir sahifadagi jadvalni CSV formatida yozish
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            # Qatorlarni bo'sh joy bilan formatlash
                            formatted_row = "    ".join([str(cell) for cell in row])
                            response.write(formatted_row + "\n")

            return response
    else:
        form = PDFUploadForm()

    return render(request, 'pdf_to_csv.html', {'form': form})
