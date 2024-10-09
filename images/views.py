import boto3
from django.shortcuts import render
from django.conf import settings
from botocore.exceptions import NoCredentialsError
from cryptography.fernet import Fernet
import os
from io import BytesIO

def generate_key():
    """Generate a key for encryption."""
    return Fernet.generate_key()

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        encrypt = request.POST.get('encrypt')  # Get the value of the checkbox

        # Initialize S3 client
        s3 = boto3.client('s3', 
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)

        try:
            if encrypt:  # If the encrypt checkbox is checked
                # Generate a key for encryption
                key = generate_key()
                cipher_suite = Fernet(key)

                # Read image content
                image_content = image.read()
                metadata = {'encrypted': 'true'}
                
                # Encrypt the image content
                encrypted_content = cipher_suite.encrypt(image_content)
                
                # Create a BytesIO object to hold the encrypted content
                encrypted_fileobj = BytesIO(encrypted_content)

                # Save the key securely (you might want to store it in a database or secure storage)
                key_filename = f"{image.name}.key"
                with open(key_filename, 'wb') as key_file:
                    key_file.write(key)

                # Upload the encrypted image to the S3 bucket
                s3.upload_fileobj(encrypted_fileobj, settings.AWS_STORAGE_BUCKET_NAME, image.name, ExtraArgs={'Metadata': metadata})
            else:
                # Upload the image file to the S3 bucket without encryption
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

    images = []  # Initialize images variable
    show_encrypted = request.GET.get('show_encrypted')  # Get filter parameter from request

    try:
        # Get the list of images from the S3 bucket
        response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        images = response.get('Contents', []) if 'Contents' in response else []

        # Filter images based on encryption metadata if the checkbox is checked
        if show_encrypted:
            images = [img for img in images if s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=img['Key']).get('Metadata', {}).get('encrypted') == 'true']
    except NoCredentialsError:
        # Log the error or handle it appropriately
        print("Credentials not available.")

    context = {
        'images': images,
        'AWS_S3_REGION_NAME': settings.AWS_S3_REGION_NAME,
        'AWS_STORAGE_BUCKET_NAME': settings.AWS_STORAGE_BUCKET_NAME,
        'show_encrypted': show_encrypted,  # Pass the filter status to the template
    }
    return render(request, 'list_images.html', context)

