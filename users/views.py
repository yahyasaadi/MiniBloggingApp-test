from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .serializers import UserRegistrationSerializer, UserLoginSerializer, BlogSerializer
from .models import Blog

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
    - Generate token here
"""
class UserLoginView(APIView):
    """This api will handle login and return token for authenticate user."""
    def post(self,request):
            serializer = UserLoginSerializer(data = request.data)
            if serializer.is_valid():
                    username = serializer.validated_data["username"]
                    password = serializer.validated_data["password"]
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        """We are reterving the token for authenticated user."""
                        # token = Token.objects.get(user=user)
                        token, created = Token.objects.get_or_create(user=user)
                        response = {
                               "status": status.HTTP_200_OK,
                               "message": "success",
                               "data": {
                                       "Token" : token.key
                                       }
                               }
                        return Response(response, status = status.HTTP_200_OK)
                    else :
                        response = {
                               "status": status.HTTP_401_UNAUTHORIZED,
                               "message": "Invalid Username or Password",
                               }
                        return Response(response, status = status.HTTP_401_UNAUTHORIZED)
            response = {
                 "status": status.HTTP_400_BAD_REQUEST,
                 "message": "bad request",
                 "data": serializer.errors
                 }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        # print('the user --- ',user)
        try:
            # Get the token for the current user
            token = Token.objects.get(user=user)
            # Delete the token
            token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            raise NotFound("Token not found for this user.")


# creating a blog
class CreateBlogView(APIView):

    """
        Create a new blog post.

        Requires authentication.

        Input:
        {
            "title": "string",
            "content": "string"
        }

        Output:
        {
            "id": 1,
            "title": "string",
            "content": "string",
            "created_at": "string",
            "author": "string"
        }
    
    """



    permission_classes = [IsAuthenticated]
    
    @cache_page(60*3)
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            cache.delete('cache_page:all-blogs')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# All blogs
class BlogList(APIView):

    @method_decorator(cache_page(60*3))
    def get(self, request):
        # print('the user----', request.user)
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Getting a single blog
class BlogDetail(APIView):
     
     def get(self, request, id):
          try:
               blog = Blog.objects.get(pk=id)
               serializer = BlogSerializer(blog)
               return Response(serializer.data, status=status.HTTP_200_OK)
          except Blog.DoesNotExist:
               return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)


# updating a blog post
class UpdateBlogView(APIView):
     """
        Update a blog post.

        Requires authentication.

        Input:
        {
            "title": "string",
            "content": "string"
        }

        Output:
        {
            "id": 1,
            "title": "string",
            "content": "string",
            "created_at": "string",
            "author": "string"
        }
     
     
     """
     permission_classes = [IsAuthenticated]

     @cache_page(60 * 3)
     def put(self, request, id):
          try:
               blog = Blog.objects.get(pk=id)
               if blog.author == request.user:
                    serializer = BlogSerializer(blog, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        cache.delete(f'cache_page:update-blog-{id}')
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               else:
                    return Response({'message': 'You are not authorized to update this blog post.'}, status=status.HTTP_403_FORBIDDEN)

          except Blog.DoesNotExist:
               return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

# deleting a blog post
class DeleteBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            blog = Blog.objects.get(pk=id)
            if blog.author == request.user:
                blog.delete()
                return Response({'message': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                 return Response({'message': 'You are not authorized to update this blog post.'}, status=status.HTTP_403_FORBIDDEN)
        except Blog.DoesNotExist:
            return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
             
          