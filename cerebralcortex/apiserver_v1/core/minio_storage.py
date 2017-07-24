from minio import Minio
from minio.error import ResponseError

minioClient = Minio('127.0.0.1:9000',
                    access_key='1UFHXT9UXEBXJ9YZA4JV',
                    secret_key='VSUFrJaovzdurcbUWsPteLs0SO857pkw29FoHDjd',
                    secure=False)


# Get a full object
# try:
#     data = minioClient.get_object('test1', '2c79b906-6f0a-40fc-8384-72b76cc18e65.mp4')
#     with open('my-testfile.mp4', 'wb') as file_data:
#         for d in data.stream(32*1024):
#             file_data.write(d)
# except ResponseError as err:
#     print(err)

buckets = minioClient.list_buckets()

for bucket in buckets:
    print(bucket.name, bucket.creation_date)