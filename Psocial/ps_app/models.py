from django.db import models
from django.contrib.auth.models import User
from polymorphic.models import PolymorphicModel


class Persona(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    universe = models.TextField(max_length=30)
    backstory = models.TextField(max_length= 300)
    avatar = models.ImageField(upload_to="ps_app/avatars")
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    
class Post(PolymorphicModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering= ['-created_at']

    def __str__(self):
        return f"Post by {self.persona} at {self.created_at}"
    
    
class TextPost(Post):
    content = models.TextField(max_length=300)

    def __str__(self):
        return f"Text post by {self.persona}: {self.content[:50]}"
    
    
class ImagePost(Post):
    image = models.ImageField(upload_to='posts/images')

    def __str__(self):
        return f"ImagePost by {self.persona}"
    
    
class ArtifactPost(Post):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"ArtifactPost by {self.persona}: {self.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.persona} on {self.post}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'persona']  
        ordering = ['-created_at']

    def __str__(self):
        return f"Like by {self.persona} on {self.post}"
    
class Clash(models.Model):
    persona1 = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='clashes_as_initiator')
    persona2 = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='clashes_as_opponent')
    topic = models.TextField()
    outcome = models.CharField(max_length=50, choices=[
        ('persona1', 'Persona 1 Wins'),
        ('persona2', 'Persona 2 Wins'),
        ('draw', 'Draw'),
    ], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['persona1', 'persona2', 'topic']  # Prevents duplicate clashes
        ordering = ['-created_at']

    def __str__(self):
        return f"Clash: {self.persona1} vs {self.persona2} on {self.topic}"
    
class UniverseMerge(models.Model):
    persona1 = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='merges_as_initiator')
    persona2 = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='merges_as_partner')
    merged_universe = models.CharField(max_length=100)  # e.g., "Pirate Galaxy"
    description = models.TextField()  # Mock AI-generated description
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['persona1', 'persona2']  # One merge per pair
        ordering = ['-created_at']

    def __str__(self):
        return f"Merge: {self.persona1.universe} + {self.persona2.universe} = {self.merged_universe}"
