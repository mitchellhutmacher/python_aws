import json
import logging
import uuid

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

s3_resource = boto3.resource("s3")
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


if __name__ == "__main__":
    dict = {}
    with open("eov-response-1595521534337.json") as f:
        dict = json.load(f)
    for i in dict["valueBlocks"]:
        print("id: {}\nlabel: {}\ndescription: {}\nvalueStatements: {}\n".format(i["id"],
        i["label"], i["description"], i["valueStatements"]))
