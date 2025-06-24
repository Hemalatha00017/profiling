from django.db import models

class MatchResult(models.Model):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=100)
    title = models.TextField()
    url = models.URLField()
    fuzzy_score = models.FloatField()
    jaccard_score = models.FloatField()
    image_score = models.FloatField()
    activity_score = models.FloatField()
    confidence = models.FloatField()
    ocr_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} on {self.platform}"
