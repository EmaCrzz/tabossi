from .models import Section

def sections(request):
    sections = Section.objects.filter(disable=False)
    return {'sections': sections}