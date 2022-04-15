#! /usr/env python3
import boto3
import argparse
from botocore.exceptions import ClientError

# Add instance id and new instance name
parser = argparse.ArgumentParser()
parser.add_argument("--instance-id", "-id", help="Instance id")
parser.add_argument("--name", "-n", help="Instance name")

# Get args
instance_id = parser.parse_args().instance_id
instance_name = parser.parse_args().name

# Get all instances filtered by instances names
client = boto3.client("ec2")
try:
	response = client.describe_instances(InstanceIds=[instance_id])
except ClientError:
	print(f"{instance_id} does not exists")
	exit()

# Now add a name to our instance
client.create_tags(Resources=[instance_id], Tags=[{"Key": "Name", "Value": instance_name}])
print(f"Instance with id {instance_id} is now tagged as {instance_name}")
