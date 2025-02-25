from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Certification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Competency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class CertificationCompetency(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

class Question(models.Model):
    text = models.TextField()
    competencies = models.ManyToManyField(Competency, related_name='questions')
    explanation = models.TextField(blank=True, null=True)
    
    def difficulty(self):
        total_attempts = self.userquestionresponse_set.count()
        correct_attempts = self.userquestionresponse_set.filter(is_correct=True).count()
        if total_attempts == 0:
            return "Unknown"
        success_rate = correct_attempts / total_attempts
        if success_rate > 0.7:
            return "Easy"
        elif success_rate > 0.4:
            return "Medium"
        return "Hard"
    
    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.question.text[:30]} - {'Correct' if self.is_correct else 'Incorrect'}"

class ExamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.certification.name} ({self.score if self.score is not None else 'In progress'})"

class UserQuestionResponse(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='question_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='correct_responses')
    is_correct = models.BooleanField()
    times_asked = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Seulement lors de la première sauvegarde
            self.times_asked += 1
            if self.is_correct:
                self.correct_attempts += 1
        super().save(*args, **kwargs)
    
    def success_rate(self):
        return (self.correct_attempts / self.times_asked * 100) if self.times_asked > 0 else 0
    
    def __str__(self):
        return f"{self.exam_session.user.username} - Q: {self.question.text[:30]} ({'Correct' if self.is_correct else 'Incorrect'})"
