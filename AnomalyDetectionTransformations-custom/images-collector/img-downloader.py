import boto3
from botocore import UNSIGNED
from botocore.config import Config


client = boto3.client('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
resource = boto3.resource('s3', region_name='eu-north-1', config=Config(signature_version=UNSIGNED))
bucket = resource.Bucket('marsanomaliedetection')


# Get list names of all photos
_BUCKET_NAME = 'marsanomaliedetection'
_PREFIX = 'DATA/'


def ListFiles(client, ls=[]):
    """List files in specific S3 URL"""
    response = client.list_objects(Bucket=_BUCKET_NAME, Prefix=_PREFIX)
    for content in response.get('Contents', []):
        ls.append(content.get('Key'))

    return ls


# test on 10 examples
# downloads photos to folder temp
count = ListFiles(client)
count = count[0:10]

for i in count:
    print(i)
    temp_img_file = 'images/{}'.format(i.split('/')[-1])
    bucket.download_file('{}'.format(i), temp_img_file)

print('Done!')
