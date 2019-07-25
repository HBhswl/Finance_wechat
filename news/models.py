from django.db import models

def post_image_path(instance, filename):
    # 图像上传的位置
    return 'img/post/{}.{}'.format(instance.id, filename.split('.')[-1])


class Post(models.Model):
    title = models.CharField(max_length=50)
    post_detail = models.TextField(blank=True)

    poster = models.ForeignKey('users.Users', on_delete=models.CASCADE)
    image = models.ImageField(max_length=256, upload_to=post_image_path, default='img/post/example/1.jpg')

    post_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    is_imported = models.BooleanField(default=True)
    if_end = models.BooleanField(default=False)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ["post_time"]

class PostLabel(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    label = models.CharField(max_length=32)

    def __str__(self):
        return '(' + str(self.post_id) + ',' + str(self.label) + ')'
