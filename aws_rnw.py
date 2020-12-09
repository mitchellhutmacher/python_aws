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
    """
    Gets a list of buckets in your AWS account

    :return: List of just names of the buckets
    """
    buckets = get_buckets()
    ret = []
    for b in buckets:
        ret.append(b.name)
    return ret


def get_json_from_bucket(bucket_name):
    """
    From each bucket, gets every file key that ends with '.json'

    Files with keys that are not their filename could be left out of this

    Args:
        bucket_name (str or list): If it's a string, it evaluates it as a single
                                   bucket.  If it's a list, it evaluates it as
                                   multiple buckets
    :return: List of JSON files in the selected buckets
    """
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
    """
    Makes a list of dictionaries from the JSON files

    From a given bucket, retrieves a given JSON file as a string, then converts
    it into a dictionary and adds it to a list.

    Args:
        key_list (list): List of keys of JSON files, along with their buckets

    :return: List of dictionaries
    """
    global conn
    ret = []
    for key in key_list:
        content = conn.get_object(Bucket=key[1], Key=key[0])['Body'].read()
        content = content.decode("utf-8")
        content = json.loads(content)
        ret.append(content)
    return ret


def make_csv(dict_list):
    """
    Creates a CSV from a list of dictionaries

    For each value statement, specify the id, label, description, statement,
    and, for each dictionary, the effectiveness and possibly importance scores.

    Args:
        dict_list (list): List of dictionaries, retrieved from AWS

    :return: String of the content of the CSV
    """
    ret = " , , , "
    for dict in dict_list:
        if dict["includeImportance"] is True:
            ret += "," + dict["email"] + ","
        else:
            ret += "," + dict["email"]
    ret += "\n"
    ret += "id,label,description,statement"
    for dict in dict_list:
        if dict["includeImportance"] is True:
            ret += ",effectiveness,importance"
        else:
            ret += ",effectiveness"
    ret += "\n"
    for block in dict_list[0]["valueBlocks"]:
        for statement in block["valueStatements"]:
            ret += block["id"] + "," + block["label"] + ","
            ret += block["description"] + ","
            ret += san_inputs(statement["statement"])
            ret += find_vals(dict_list, block["id"], statement["statement"])
            ret += "\n"
    return ret


def find_vals(dict_list, block, statement):
    """
    Finds the values for a statement

    The statement is in every JSON file, it can either have an effectiveness
    score or both an effectiveness and an importance score.

    Args:
    dict_list (list): List of dictionaries, retrieved from AWS
    block (String): String of which block the statement belongs to
    statement (String): The statement

    :return: The effectiveness and importance of the given statement
    """
    ret = ","
    imp = []
    for dict in dict_list:
        imp.append(dict["includeImportance"])
    for i, dict in enumerate(dict_list):
        for the_block in dict["valueBlocks"]:
            if the_block["id"] == block:
                for the_statement in the_block["valueStatements"]:
                    if the_statement["statement"] == statement:
                        if imp[i] == True:
                            ret += str(the_statement["effectiveness"]) + ","
                            ret += str(the_statement["importance"]) + ","
                        else:
                            ret += str(the_statement["effectiveness"]) + ","
    ret = ret[0:len(ret)-1]
    return ret


def san_inputs(statement):
    """
    Makes the statement easier to read in a CSV

    Adds quotation marks around a statement so that if there is a character,
    such as a comma, the CSV won't read that as a new entry.  This is only
    important for reading CSV files in programs like Excel.

    Args:
        statement (String): The value statement

    :return: The value statement with quotation marks
    """
    statement = "\"" + statement + "\""
    return statement


if __name__ == "__main__":
    dict = {}
    buckets = list_of_buckets()
    json_objs = []
    json_objs = get_json_from_bucket(buckets)
    all_dicts = make_json_list(json_objs)
    ret = make_csv(all_dicts)
