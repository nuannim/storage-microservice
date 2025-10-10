from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json
import os



@api_view(['GET'])
def download_image_by_filename(request, filename):
    """API endpoint for downloading an image by path (/images/filename.ext)"""
    # ตัด /images/ ออก ถ้ามี
    if filename.startswith('images/'):
        filename = filename[len('images/'):]
    elif filename.startswith('/images/'):
        filename = filename[len('/images/'):]
    file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    if not os.path.exists(file_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@api_view(['POST'])
def upload_image(request):
    """API endpoint for uploading images (no database)"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    file = request.FILES['file']
    images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    os.makedirs(images_dir, exist_ok=True)
    file_path = os.path.join(images_dir, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return Response({
        'filename': file.name,
        'url': request.build_absolute_uri(f'/media/images/{file.name}')
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_image(request, filename):
    """API endpoint for retrieving image information (no database)"""
    # ตัด /images/ ออก ถ้ามี
    if filename.startswith('images/'):
        filename = filename[len('images/'):]
    elif filename.startswith('/images/'):
        filename = filename[len('/images/'):]
    file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    if not os.path.exists(file_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    size = os.path.getsize(file_path)
    return Response({
        'filename': filename,
        'size': size,
        'url': request.build_absolute_uri(f'/media/images/{filename}')
    })

@api_view(['GET'])
def download_image(request, filename):
    """API endpoint for downloading an image (no database)"""
    # ตัด /images/ ออก ถ้ามี
    if filename.startswith('images/'):
        filename = filename[len('images/'):]
    elif filename.startswith('/images/'):
        filename = filename[len('/images/'):]
    file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    if not os.path.exists(file_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

@api_view(['DELETE'])
def delete_image(request, filename):
    """API endpoint for deleting an image (no database)"""
    # ตัด /images/ ออก ถ้ามี
    if filename.startswith('images/'):
        filename = filename[len('images/') :]
    elif filename.startswith('/images/'):
        filename = filename[len('/images/') :]
    file_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
    if not os.path.exists(file_path):
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    os.remove(file_path)
    return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_images(request):
    """API endpoint for listing all images in media/images/ (no database)"""
    images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    if not os.path.exists(images_dir):
        return Response([])
    files = os.listdir(images_dir)
    data = []
    for filename in files:
        file_path = os.path.join(images_dir, filename)
        if os.path.isfile(file_path):
            data.append({
                'filename': filename,
                'url': request.build_absolute_uri(f'/media/images/{filename}')
            })
    return Response(data)
