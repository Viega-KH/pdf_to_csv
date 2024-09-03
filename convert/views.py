import csv
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

            # CSV yozuvchi yaratish
            writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            try:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        if tables:
                            for table in tables:
                                for row in table:
                                    # Har bir hujayrani to'g'ri formatlash
                                    cleaned_row = [str(cell).strip() if cell else '' for cell in row]
                                    writer.writerow(cleaned_row)
                return response
            except Exception as e:
                return HttpResponse(f"Xatolik yuz berdi: {str(e)}", status=500)
    else:
        form = PDFUploadForm()

    return render(request, 'pdf_to_csv.html', {'form': form})
