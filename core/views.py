import random
import time
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import os

from rev_ai import apiclient

from rev_ai import JobStatus

from record.settings import BASE_DIR
from record.utils import load_env

from .models import Record

load_env(BASE_DIR / ".env") #here you indicate where your .env file is

token = os.environ.get("REV_API_KEY")


def record(request):
    transcript_text = "text"
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")

        language = request.POST.get("language")

        record = Record.objects.create(
            language=language,
            voice_record=audio_file,
        )

        record.save()

        client = apiclient.RevAiAPIClient(token)
        job = client.submit_job_local_file(str(BASE_DIR) + record.voice_record.url)

        job_details = client.get_job_details(job.id)

        while (job_details.status == JobStatus.IN_PROGRESS):
            job_details = client.get_job_details(job.id)
            time.sleep(1)
            print(job_details.status)

        # retrieve transcript as text
        transcript_text = client.get_transcript_text(job.id)

        transcript_text = parse_text(transcript_text)

        record.transcript = transcript_text

        record.result = detect_alzheimers(transcript_text)

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


def detect_alzheimers(transcript):
    # send the audio to remote api for processing
    words = transcript.split(" ")

    if (len(words) > 50):
        return "Healthy"
    return "Likely Dementia"

def parse_text(transcript):
    return transcript[21:]

def delete_audio(request, id):
    audio_record = get_object_or_404(Record, id=id)

    # Delete file using this: record.voice_record.url
    if os.path.isfile(str(BASE_DIR) + audio_record.voice_record.url):
        os.remove(str(BASE_DIR) + audio_record.voice_record.url)
    audio_record.delete()

    return index(request)
