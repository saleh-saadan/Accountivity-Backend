from django.db import models
from django.conf import settings


class TDList(models.Model):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_lists",
    )

    # Specifies all friends the list is shared with
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="shared_lists",
    )

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "TDLists"

    def __str__(self):
        return self.name


class Task(models.Model):

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Connects the task to a particular list
    list = models.ForeignKey(
        "TDList",
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    name = models.CharField(max_length=200)

    completed = models.BooleanField(default=False)

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
