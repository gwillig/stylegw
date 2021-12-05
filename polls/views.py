from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from .helper import tensor_to_image, imshow, load_img
from .models import Choice, Question
from django.http import FileResponse
# '=========='
# import os
# import PIL.Image
# import numpy as np
# import matplotlib.pyplot as plt
# # import tensorflow as tf
# import tensorflow_hub as hub
# # Load compressed models from tensorflow_hub
# os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'
# '=================='
#

def send_file(response):
    return HttpResponse("hello")
# def send_file(response):
#
#     # img = open('Download.png', 'rb')
#     url = [
#         "https://lh3.googleusercontent.com/HnyXa-dNoEu_ouZ_O_uuofcVNRgJ1MqCuHUTxxzlo25uAtvYXl8kZiLRtaLk8IdGSGp1cOJOhNg5sboSGCXKEwtw0Q8PyNRSinhjt6ev8ABeAonagKeLNIeWAtp52I66RXeTySYxrwE=w2400",
#     ]
#     orginal_imge = [
#         "https://lh3.googleusercontent.com/pw/AM-JKLUTeYR5V2-SfH6yO46pFU9kMMGD2t9Y0n6-9w8ln4X7yZuAR_uK02QPp-cBBaebYzVEkPQh_KGvdDYXmSOsaLcfuH2KPTTv4TUwYHjWffbB29sshldNtnS4IywZMdCTdgw0hNDWH60Lmui3FLDnzlCiDQ=w509-h679-no?authuser=0"]
#     content_image = tf.keras.utils.get_file("content_image", orginal_imge[0])
#     plt.figure(figsize=(60, 6))
#
#     content_image = load_img(content_image)
#
#     recreate = True
#     for el in url:
#         '#Check if file is from google'
#         if el.find("google") != -1:
#             'Down size image'
#             el = el.replace("w2400", "w500")
#             'Remove special characters'
#             fname = el.split("/")[-1]
#             for char in ["-", "="]:
#                 fname = fname.replace(char, "_")
#             fname = fname + ".jpg"
#
#
#         else:
#             fname = el.split("/")[-1]
#         style_path = tf.keras.utils.get_file(fname, el)
#         style_image = load_img(style_path)
#
#         '#Check if style has beedn already used'
#         fname_result = "result_" + fname
#
#         hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
#         stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
#         result = tensor_to_image(stylized_image)
#
#     response = FileResponse(result)
#
#     return response


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Update the model, excluding any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
