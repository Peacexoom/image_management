import boto3
from django.shortcuts import render, redirect
from django.conf import settings
import boto3
from botocore.exceptions import NoCredentialsError

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        # Initialize S3 client
        s3 = boto3.client('s3', 
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)

        try:
            # Upload the image file to the S3 bucket
            s3.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, image.name)
            return render(request, 'upload_image.html', {'success': True})
        except NoCredentialsError:
            return render(request, 'upload_image.html', {'error': 'Error: Credentials not available.'})
    return render(request, 'upload_image.html')

def list_images(request):
    s3 = boto3.client('s3', 
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      region_name=settings.AWS_S3_REGION_NAME)

    # Get the list of images from the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        images = response.get('Contents', []) if 'Contents' in response else []
    except NoCredentialsError:
        images = []

    return render(request, 'list_images.html', {'images': images})
