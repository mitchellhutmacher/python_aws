import json
import logging
import uuid
import io

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

s3_resource = boto3.resource("s3")
conn = boto3.client("s3")
"""
https://docs.aws.amazon.com/code-samples/latest/catalog/
python-s3-s3_basics-bucket_wrapper.py.html
"""

def get_s3(region=None):
    """Get a Boto 3 S3 resource with a specific Region or with your default Region."""
    global s3_resource
    if not region or s3_resource.meta.client.meta.region_name == region:
        return s3_resource
    else:
        return boto3.resource('s3', region_name=region)


def bucket_exists(bucket_name):
    """
    Determine whether a bucket with the specified name exists.

    Usage is shown in usage_demo at the end of this module.

    :param bucket_name: The name of the bucket to check.
    :return: True when the bucket exists; otherwise, False.
    """
    s3 = get_s3()
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        logger.info("Bucket %s exists.", bucket_name)
        exists = True
    except ClientError:
        logger.warning("Bucket %s doesn't exist or you don't have access to it.",
                       bucket_name)
        exists = False
    return exists


def get_buckets():
    """
    Get the buckets in all Regions for the current account.

    Usage is shown in usage_demo at the end of this module.

    :return: The list of buckets.
    """
    s3 = get_s3()
    try:
        buckets = list(s3.buckets.all())
        logger.info("Got buckets: %s.", buckets)
    except ClientError:
        logger.exception("Couldn't get buckets.")
        raise
    else:
        return buckets


def list_of_buckets():
    buckets = get_buckets()
    ret = []
    for b in buckets:
        ret.append(b.name)
    return ret


def get_json_from_bucket(bucket_name):
    json_list = []
    global conn
    if isinstance(bucket_name, str):
        for key in conn.list_objects(Bucket=bucket_name)['Contents']:
            if key['Key'].endswith(".json"):
                json_list.append([key['Key'], bucket])
        return json_list
    elif isinstance(bucket_name, list):
        for bucket in bucket_name:
            for key in conn.list_objects(Bucket=bucket)['Contents']:
                if key['Key'].endswith(".json"):
                    json_list.append([key['Key'], bucket])
            return json_list

def make_json_list(key_list):
    global conn
    ret = []
    for key in key_list:
        content = conn.get_object(Bucket=key[1], Key=key[0])['Body'].read()
        content = content.decode("utf-8")
        content = json.loads(content)
        ret.append(content)
        print(type(content))
    return ret


def make_csv(dict_list):
    ret = ""
    return ret


if __name__ == "__main__":
    dict = {}
    buckets = list_of_buckets()
    json_objs = []
    # for bucket in buckets:
    #     jsons = get_json_from_bucket(bucket)
    #     json_objs += jsons
    json_objs = get_json_from_bucket(buckets)
    all_dicts = make_json_list(json_objs)
    # for dict in all_dicts:
    #     print(dict)
    # test = io.StringIO()
    # test = conn.get_object(Bucket=bucket, Key=json_objs[0])
    # test['Body'].read()
