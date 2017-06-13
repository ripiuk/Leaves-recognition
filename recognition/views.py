from django.views import generic
from .forms import RecognitionImageForm
from .models import Recognition, Tree
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from recognition.what_leaf_is import label_image
from functools import reduce
from django.db.models import Q, Count
import operator


class IndexView(generic.FormView):
    template_name = 'recognition/index.html'
    form_class = RecognitionImageForm

    def form_valid(self, form):
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


"""class ShowTrees(generic.ListView):
    template_name = 'recognition/all_tree.html'
    context_object_name = 'all_tree'
    paginate_by = 8

    def get_queryset(self):
        return Tree.objects.all().order_by('id')"""

def show_trees(request):
    all_tree = Tree.objects.all().order_by('id')
    maple = Recognition.objects.filter(tree=all_tree[0]).count()
    birch = Recognition.objects.filter(tree=all_tree[1]).count()
    willow = Recognition.objects.filter(tree=all_tree[2]).count()
    context = {
        'all_tree': all_tree,
        'maple': maple,
        'birch': birch,
        'willow': willow,
    }
    return render(request, 'recognition/all_tree.html', context)


"""class TheTree(generic.DetailView):
    template_name = 'recognition/tree_detail.html'
    model = Tree
    pk_url_kwarg = 'id'

    def lol2(self):
        return self.kwargs['id']

    #lol = Recognition.objects.filter(tree=Tree.objects.filter(id=lol2))"""


def the_tree(request, id=None):
    instance = get_object_or_404(Tree, id=id)
    images = Recognition.objects.filter(tree=instance)
    context = {
        'tree': instance,
        'images': images,
    }
    return render(request, 'recognition/tree_detail.html', context)





class PersonalAcc(generic.ListView):
    template_name = 'recognition/personal_account.html'
    context_object_name = 'account_img'
    paginate_by = 8

    def get_queryset(self):
        return Recognition.objects.filter(user=self.request.user)


class SearchList(generic.ListView):
    template_name = 'recognition/search_res.html'
    context_object_name = 'res'
    paginate_by = 8

    def get_queryset(self):
        res = Recognition.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            res = res.filter(
                reduce(operator.and_,
                       (Q(tree__title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(user__username__icontains=q) for q in query_list))
            )
        return res
