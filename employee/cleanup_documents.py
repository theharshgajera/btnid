from django.core.management.base import BaseCommand
from .models import Document
from collections import defaultdict

class Command(BaseCommand):
    help = 'Clean up duplicate Document entries'

    def handle(self, *args, **kwargs):
        documents = Document.objects.all()
        documents_by_employee = defaultdict(list)

        for document in documents:
            documents_by_employee[document.employee_id].append(document)

        for employee_id, docs in documents_by_employee.items():
            if len(docs) > 1:
                # Keep the first document and delete the rest
                primary_doc = docs[0]
                for doc in docs[1:]:
                    if doc.aadhaar_card and not primary_doc.aadhaar_card:
                        primary_doc.aadhaar_card = doc.aadhaar_card
                    if doc.pan_card and not primary_doc.pan_card:
                        primary_doc.pan_card = doc.pan_card
                    if doc.light_bill and not primary_doc.light_bill:
                        primary_doc.light_bill = doc.light_bill
                    if doc.photo and not primary_doc.photo:
                        primary_doc.photo = doc.photo
                    doc.delete()
                primary_doc.save()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned up duplicate Document entries'))
