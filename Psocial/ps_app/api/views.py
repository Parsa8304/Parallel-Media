from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from .throttling import InteractionThrottle
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsUniverseMemberOrPublic
from ps_app.models import Persona, Post, TextPost, ImagePost, ArtifactPost, Comment, Like, Clash, UniverseMerge
from .serializers import (
    PersonaSerializer, PostPolymorphicSerializer, TextPostSerializer, ImagePostSerializer,
    ArtifactPostSerializer, CommentSerializer, LikeSerializer, ClashSerializer, UniverseMergeSerializer
)


class UserRegisterView(APIView):
    """
    View to handle user registration.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=400)
        
        user = User.objects.create_user(username=username, password=password)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def discover(self, request):
        tags = request.query_params.get('tags', '').split(',')
        if tags[0]:
            queryset = Persona.objects.filter(tags__icontains=tags[0])
            for tag in tags[1:]:
                queryset |= Persona.objects.filter(tags__icontains=tag)
        else:
            queryset = Persona.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostPolymorphicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUniverseMemberOrPublic]

    def perform_create(self, serializer):
        serializer.save(persona=self.request.user.persona)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUniverseMemberOrPublic]
    throttle_classes = [InteractionThrottle]

    def perform_create(self, serializer):
        serializer.save(persona=self.request.user.persona)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsUniverseMemberOrPublic]
    throttle_classes = [InteractionThrottle]

    def perform_create(self, serializer):
        serializer.save(persona=self.request.user.persona)

class ClashViewSet(viewsets.ModelViewSet):
    queryset = Clash.objects.all()
    serializer_class = ClashSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        clash = self.get_object()
        outcome = request.data.get('outcome')
        if outcome in ['persona1', 'persona2', 'draw']:
            clash.outcome = outcome
            clash.save()
            serializer = self.get_serializer(clash)
            return Response(serializer.data)
        return Response({'error': 'Invalid outcome'}, status=400)

class UniverseMergeViewSet(viewsets.ModelViewSet):
    queryset = UniverseMerge.objects.all()
    serializer_class = UniverseMergeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        persona1 = self.request.user.persona
        persona2_id = self.request.data.get('persona2')
        persona2 = Persona.objects.get(id=persona2_id)
        merged_universe = f"{persona1.universe} + {persona2.universe}"
        description = f"In the merged universe of {merged_universe}, the worlds of {persona1.universe} and {persona2.universe} intertwine, creating a unique realm where {persona1.universe.lower()} meets {persona2.universe.lower()}."
        serializer.save(persona1=persona1, persona2=persona2, merged_universe=merged_universe, description=description)
