from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from ps_app.models import Persona, Post, TextPost, ImagePost, ArtifactPost, Comment, Like, Clash, UniverseMerge
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class PersonaSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = ['id', 'user', 'universe', 'backstory', 'avatar', 'tags', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'persona', 'created_at', 'updated_at', 'is_public']

class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = ['id', 'persona', 'content', 'created_at', 'updated_at', 'is_public']

class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['id', 'persona', 'image', 'created_at', 'updated_at', 'is_public']

class ArtifactPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtifactPost
        fields = ['id', 'persona', 'name', 'description', 'created_at', 'updated_at', 'is_public']

class PostPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Post: PostSerializer,
        TextPost: TextPostSerializer,
        ImagePost: ImagePostSerializer,
        ArtifactPost: ArtifactPostSerializer,
    }

    class Meta:
        model = Post
        fields = ['id', 'persona', 'created_at', 'updated_at', 'is_public']

class CommentSerializer(serializers.ModelSerializer):
    post = PostPolymorphicSerializer(read_only=True)
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'persona', 'content', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    post = PostPolymorphicSerializer(read_only=True)
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'post', 'persona', 'created_at']

class ClashSerializer(serializers.ModelSerializer):
    persona1 = PersonaSerializer(read_only=True)
    persona2 = PersonaSerializer(read_only=True)

    class Meta:
        model = Clash
        fields = ['id', 'persona1', 'persona2', 'topic', 'outcome', 'created_at']

class UniverseMergeSerializer(serializers.ModelSerializer):
    persona1 = PersonaSerializer(read_only=True)
    persona2 = PersonaSerializer(read_only=True)

    class Meta:
        model = UniverseMerge
        fields = ['id', 'persona1', 'persona2', 'merged_universe', 'description', 'created_at']