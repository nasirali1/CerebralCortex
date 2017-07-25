# Copyright (c) 2017, MD2K Center of Excellence
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from minio import Minio
from minio.error import ResponseError
import json
from pytz import timezone

class MinioStorage:
    def __init__(self, CC_obj):

        self.CC_obj = CC_obj
        self.configuration = CC_obj.configuration
        self.hostIP = self.configuration['cassandra']['host']
        self.localtz = timezone(self.CC_obj.time_zone)
        self.minioClient = Minio(str(self.configuration['minio']['host'])+":"+str(self.configuration['minio']['port']),
                            access_key=self.configuration['minio']['access_key'],
                            secret_key=self.configuration['minio']['secret_key'],
                            secure=self.configuration['minio']['secure'])

    # Get a full object
    def get_object(self, bucket_name, object_name):
        try:
            data = self.minioClient.get_object(bucket_name, object_name)
            with open('my-testfile.mp4', 'wb') as file_data:
                for d in data.stream(32*1024):
                    file_data.write(d)
        except ResponseError as err:
            return str(err)

    def list_buckets(self):
        bucket_list = {}
        buckets = self.minioClient.list_buckets()
        for bucket in buckets:
            bucket_list[bucket.name] = {"last_modified": str(bucket.creation_date.replace(tzinfo=self.localtz))}
        return bucket_list

    def list_objects_in_bucket(self, bucket_name):
        # List all object paths in bucket that begin with my-prefixname.
        objects_in_bucket = {}
        try:
            objects = self.minioClient.list_objects(bucket_name, recursive=True)
            for obj in objects:
                objects_in_bucket[obj.object_name] = {"last_modified": str(obj.last_modified.replace(tzinfo=self.localtz)), "size":obj.size, "content_type": obj.content_type, "etag": obj.etag}
            return objects_in_bucket
        except Exception as e:
            objects_in_bucket["error"] = str(e).replace("NoSuchBucket: message: ", "").replace("InvalidBucketError: message: ", "")
            return objects_in_bucket

    def get_object_stat(self, bucket_name, object_name):
        object_stat = {}
        try:
            if self.bucket_exist(bucket_name):
                object_stat = self.minioClient.stat_object(bucket_name, object_name)
                object_stat = json.dumps(object_stat, default=lambda o: o.__dict__)
                return object_stat
            else:
                object_stat["error"] = "Bucket does not exist"
                return object_stat

        except Exception as err:
            object_stat["error"] = str(err).replace("NoSuchKey: message: ", "")
            return object_stat

    def get_object(self, bucket_name, object_name):
        object = {}
        try:
            if self.bucket_exist(bucket_name):
                object = self.minioClient.get_object(bucket_name, object_name)

                return object
            else:
                object["error"] = "Bucket does not exist"
                return object

        except Exception as err:
            object["error"] = str(err).replace("NoSuchKey: message: ", "")
            return object

    def bucket_exist(self, bucket_name):
        try:
            return self.minioClient.bucket_exists(bucket_name)
        except ResponseError as err:
            return err