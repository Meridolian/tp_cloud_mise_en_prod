#! /usr/env python3
import boto3
import argparse

# Add tags arguments
parser = argparse.ArgumentParser()
parser.add_argument("--tag-name", help="Tag Name")
parser.add_argument("--tag-value", help="Tag Value")

# Get args
tag_name = parser.parse_args().tag_name
tag_value = parser.parse_args().tag_value

# Get all instances filtered by tag
client = boto3.client("ec2")
filters = [{"Name": f"tag:{tag_name}", "Values": [tag_value]}]
response = client.describe_instances(Filters=filters)

# Get ids of instances
instances_ids = []
instances_names = []
for instance in response["Reservations"][0]["Instances"]:
	instances_ids.append(instance["InstanceId"])
	for tag in instance["Tags"]:
		if tag["Key"] == "Name":
			instances_names.append(tag["Value"])

# Stop instances by their ids
client.stop_instances(InstanceIds=instances_ids)
print(f"{' '.join(instances_names)} has been stopped")
