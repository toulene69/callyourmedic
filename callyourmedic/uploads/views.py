
from callyourmedic.settings import BASE_DIR
from utils.app_utils import uniqid
from callyourmedic.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection
import os


import traceback
import logging

logger = logging.getLogger('webportal')
# Create your views here.
TEMP_PATH = BASE_DIR + '/uploads/temp/'
BUCKET_NAME = 'callyourmedic-branding-resources'

def s3_get_connection():
    return S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

def handle_uploaded_file(file):

    if file is None:
        return
    unique_name = uniqid('dept_',True) + '_' + file.name
    file_path = TEMP_PATH + unique_name
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        status = s3_upload_dept(file_path,unique_name)
        if status is True:
            delete_file_local(file_path)
            return unique_name
        return None
    except:
        traceback.print_exc()
        return None

def handle_delete_file(disk_name):
    """Deletes a file from s3 with the give disk_name on s3 """
    if disk_name:
        folder = 'departments/'
        key = folder+disk_name
        s3_delete_file(key)

def s3_upload_dept(file,filename):

    folder = 'departments/'
    try:
        connection = s3_get_connection()
        bucket = connection.get_bucket(BUCKET_NAME)
        k = Key(bucket)
        k.key = folder+filename
        k.set_contents_from_filename(file)
        k.set_acl('public-read')
        return True
    except:
        traceback.print_exc()
        return False

def s3_delete_file(key):

    try:
        connection = s3_get_connection()
        bucket = connection.get_bucket(BUCKET_NAME)
        possible_key = bucket.get_key(key)
        possible_key.delete()

    except:
        traceback.print_exc()
        raise Exception

def delete_file_local(file_path):
    try:
        os.remove(file_path)
    except:
        logger.error("Error while deleting file.")
        traceback.print_exc()
