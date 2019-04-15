from django.db import models


class Post(models.Model):
    """
    make a textfield model to store the contents
    of the user input.
    and a publish date, for posting the contents order by date and time
    """
    content = models.TextField(default="default text")
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.content
