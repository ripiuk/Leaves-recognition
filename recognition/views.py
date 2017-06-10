from django.views import generic
from .forms import RecognitionImageForm
from .models import Recognition
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from recognition.what_leaf_is import label_image


class IndexView(generic.FormView):
    template_name = 'recognition/index.html'
    form_class = RecognitionImageForm

    def form_valid(self, form):
        recognition_image = Recognition(image=self.get_form_kwargs().get('files')['image'])
        recognition_image.save()
        self.id = recognition_image.id
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recognition:recognition', kwargs={'id': self.id})


def recognition(request, id=None):
    instance = get_object_or_404(Recognition, id=id)
    result = label_image.recognition(instance.image.path)
    context = {
        'image': instance.image,
        'instance': instance,
        'result': result,
        'first_label': result[0],
        'first_score': result[1],
        'second_label': result[2],
        'second_score': result[3],
    }
    return render(request, 'recognition/recognition.html', context)

