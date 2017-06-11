from django.views import generic
from .forms import RecognitionImageForm
from .models import Recognition, Tree
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from recognition.what_leaf_is import label_image

result = []


class IndexView(generic.FormView):
    template_name = 'recognition/index.html'
    form_class = RecognitionImageForm

    def form_valid(self, form):
        global result
        recognition_image = Recognition(image=self.get_form_kwargs().get('files')['image'])
        recognition_image.save()
        result = label_image.recognition(recognition_image.image.path)
        recognition_image.tree = Tree.objects.get(title=result[0])
        recognition_image.result = ', '.join(str(i) for i in result)
        if self.request.user.is_authenticated():
            recognition_image.user = self.request.user
        else:
            recognition_image.user = None
        recognition_image.save()
        self.id = recognition_image.id
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('recognition:recognition', kwargs={'id': self.id})


def recognition(request, id=None):
    instance = get_object_or_404(Recognition, id=id)
    result = instance.result.split(', ')
    context = {
        'image': instance.image,
        'tree': instance.tree,
        'result': result,
    }
    return render(request, 'recognition/recognition.html', context)


class ShowAll(generic.ListView):
    template_name = 'recognition/all_pic.html'
    context_object_name = 'all_images'
    paginate_by = 8

    def get_queryset(self):
        return Recognition.objects.all().order_by('-id')


class PersonalAcc(generic.ListView):
    template_name = 'recognition/personal_account.html'
    context_object_name = 'account_img'
    paginate_by = 8

    def get_queryset(self):
        return Recognition.objects.filter(user=self.request.user)
