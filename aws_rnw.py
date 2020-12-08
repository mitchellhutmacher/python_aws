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


if __name__ == "__main__":
    dict = {}
    with open("eov-response-1595521534337.json") as f:
        dict = json.load(f)
    for i in dict["valueBlocks"]:
        print("id: {}\nlabel: {}\ndescription: {}\nvalueStatements: {}\n".format(i["id"],
        i["label"], i["description"], i["valueStatements"]))
