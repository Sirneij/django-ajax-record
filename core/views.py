import random
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Record


def record(request):
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        result = detect_alzheimers(audio_file)
        language = request.POST.get("language")
        record = Record.objects.create(language=language, voice_record=audio_file, result=result)
        record.save()
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "url": record.get_absolute_url(),
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}

    return render(request, "core/record.html", context)

def record_detail(request, id):
	# fetch the results from the remote server
	# display it here
    record = get_object_or_404(Record, id=id)
    context = {
        "page_title": "Recorded audio detail",
        "record": record,
    }
	
    return render(request, "core/record_detail.html", context)


def index(request):
    records = Record.objects.all()
    context = {"page_title": "Voice records", "records": records}
    return render(request, "core/index.html", context)


def detect_alzheimers(audio_file):
	# send the audio to remote api for processing
	detection = ["Yes", "No", "Maybe"]

	idx = random.randint(0, 2)
	return detection[idx]