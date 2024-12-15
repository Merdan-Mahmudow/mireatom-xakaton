#!/usr/bin/env python
#-*- coding: utf-8 -*-
import io
from typing import List
import uuid

from app.core.config import settings
from fastapi import UploadFile
import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

# Загрузить объекты в бакет

## Из файла
async def get_url(file: List[UploadFile]):
	uploded_files = []
	filenames = []
	file_urls = []
	for f in file:
		file_content = await f.read()
		f.filename = f'{uuid.uuid4()}.{f.filename.split(".")[-1]}'
		filenames.append(f.filename)
		s3.upload_fileobj(
			Fileobj=io.BytesIO(file_content),
			Bucket=f'{settings.YANDEX_BUCKET_NAME}',
			Key=f.filename
		)
		uploded_files.append({"filename": f.filename, "status": "uploaded"})
	async def get(img_url):
		return [f"https://storage.yandexcloud.net/{settings.YANDEX_BUCKET_NAME}/" + uploded_files[f]["filename"] for f in range(len(uploded_files))]
	return await get(filenames)
		
async def get_url_base64(base):
	filename = f'{uuid.uuid4()}.jpg'
	s3.upload_fileobj(
		Fileobj=io.BytesIO(base),
		Bucket=f'{settings.YANDEX_BUCKET_NAME}',
		Key=filename
	)
	return f"https://storage.yandexcloud.net/{settings.YANDEX_BUCKET_NAME}/{filename}"


# ## Из файла
async def upload_file_to_s3(file: List[UploadFile]):
	uploded_files = []
	filenames = []
	file_urls = []
	for f in file:
		file_content = await f.read()
		f.filename = str(uuid.uuid4()) + ".jpg"
		filenames.append(f.filename)
		s3.upload_fileobj(
			Fileobj=io.BytesIO(file_content),
			Bucket='cluddy-bucket',
			Key=f.filename
		)
		uploded_files.append({"filename": f.filename, "status": "uploaded"})
	async def get_url_from_s3(files: List[str]):
		for f in files:
			url = s3.generate_presigned_url(
				ClientMethod='get_object',
				Params={'Bucket': 'cluddy-bucket', 'Key': f}
			)
			file_urls.append({"filename": f, "url": url})
		return file_urls		
	return await get_url_from_s3(filenames)


# Получить список объектов в бакете
def get_objects_s3():
	for key in s3.list_objects(Bucket='bucket-name')['Contents']:
		print(key['Key'])

