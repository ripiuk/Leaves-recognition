from django.db import models


class Tree(models.Model):
    title = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='trees')

    def __str__(self):
        return str(self.title).upper()


class Recognition(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='recognitions')
    result = models.CharField(max_length=250, null=Tree)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.tree).upper() + ' ' + str(self.created_at)
