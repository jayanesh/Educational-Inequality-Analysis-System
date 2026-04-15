from djongo import models

class SchoolData(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    year = models.IntegerField()
    school_level = models.CharField(max_length=50) # Primary, Secondary, etc.
    gender = models.CharField(max_length=20) # Male, Female, Total
    social_category = models.CharField(max_length=50, default='General') # SC, ST, OBC, General
    dropout_rate = models.FloatField()
    
    # Influencing Factors
    infrastructure_index = models.FloatField(default=0.0) # 0-100
    poverty_ratio = models.FloatField(default=0.0) # % of population below poverty line
    literacy_rate = models.FloatField(default=0.0)
    pupil_teacher_ratio = models.FloatField(default=0.0)
    
    class Meta:
        verbose_name_plural = "School Data Records"

    def __str__(self):
        return f"{self.state} - {self.district} ({self.year})"
