# Image Upload and Listing Application

## Overview

The **Image Upload and Listing Application** is a Django web application that allows users to upload images to an AWS S3 bucket and list all uploaded images with download options. This project demonstrates how to integrate AWS services using Boto3, enabling users to manage their images seamlessly through a user-friendly interface.

## Features

- **Image Upload**: Users can upload images which are then stored in an AWS S3 bucket.
- **Image Listing**: A dedicated page displays all uploaded images with links to download each image.
- **Feedback Mechanism**: Users receive feedback upon successful uploads or any errors encountered.
- **Encypted Images**: Users can store encrypted images and filer those images.

## Technologies Used

- **Django**: A high-level Python web framework for building web applications.
- **AWS S3**: A scalable object storage service for storing uploaded images.
- **Boto3**: The Amazon Web Services (AWS) SDK for Python, used for all interactions with AWS services.
- **EC2**: Elastic Compute Cloud, used to host the application.
