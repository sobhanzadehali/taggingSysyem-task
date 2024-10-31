from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Dataset(models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"))

    def __str__(self):
        return self.name


class Operator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class HasPermission(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "permission"
        verbose_name_plural = "permissions"

    def __str__(self):
        return f"{self.dataset.name} - {self.operator.user.username}"


class Tag(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=255)
    is_active = models.BooleanField(_("is_active"), default=False)

    def __str__(self):
        return self.name


class Sentence(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(_("body"))

    def __str__(self):
        return f"{self.body[:50]}..."


class LabeledSentence(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sentence[:50]}, {self.tag[:50]}"
