# from minio import Minio
# from minio.error import ResponseError
# import json
# minioClient = Minio('127.0.0.1:9000',
#                     access_key='1UFHXT9UXEBXJ9YZA4JV',
#                     secret_key='VSUFrJaovzdurcbUWsPteLs0SO857pkw29FoHDjd',
#                     secure=False)
#
#
# # Get a full object
# def get_object(bucket_name, object_name):
#     try:
#         data = minioClient.get_object(bucket_name, object_name)
#         with open('my-testfile.mp4', 'wb') as file_data:
#             for d in data.stream(32*1024):
#                 file_data.write(d)
#     except ResponseError as err:
#         print(err)
#
# def list_buckets():
#     bucket_list = {}
#     buckets = minioClient.list_buckets()
#
#     for bucket in buckets:
#         bucket_list[bucket.name] = bucket.creation_date
#     return bucket_list
#
#
#
# def get_object_stat(bucket_name, object_name):
#     try:
#         if(bucket_exist(bucket_name)):
#             object_stat = minioClient.stat_object(bucket_name, object_name)
#             object_stat = json.dumps(object_stat, default=lambda o: o.__dict__)
#             return object_stat
#         else:
#             return "Bucket does not exist"
#     except Exception as err:
#         print(err)
#
# def bucket_exist(bucket_name):
#     try:
#         print(minioClient.bucket_exists(bucket_name))
#     except ResponseError as err:
#         print(err)
#
# bucket_exist("test1e")
#
# ss =get_object_stat("test1", "2c79b906-6f0a-40fc-8384-72b76cc18e65.mp4")
# print(ss)