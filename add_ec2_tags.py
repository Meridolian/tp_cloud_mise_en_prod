#! /usr/env python3
import boto3
import argparse

# Add instances names and tags arguments
parser = argparse.ArgumentParser()
parser.add_argument("--instances", nargs="+", default=[], help="List of EC2 instances name")
parser.add_argument("--tag-name", help="Tag Name to add to instances")
parser.add_argument("--tag-value", help="Tag Value to add to instances")

# Get args
instances = parser.parse_args().instances
tag_name = parser.parse_args().tag_name
tag_value = parser.parse_args().tag_value

# Get all instances filtered by instances names
client = boto3.client("ec2")
filters = [{"Name": "tag:Name", "Values": instances}]
response = client.describe_instances(Filters=filters)

# Get instances names found
instances_names = []
instances_ids = []
for instance in response["Reservations"][0]["Instances"]:
	instances_ids.append(instance["InstanceId"])
	for tag in instance["Tags"]:
		if tag["Key"] == "Name":
			instances_names.append(tag["Value"])

# Compare them to find if an instance in arguments does not exists
# If 1 or more instances dont exists, print them and exit
instances_not_found = []
for instance in instances:
	if instance not in instances_names:
		instances_not_found.append(instance)
if len(instances_not_found) > 0:
	for i in instances_not_found:
		print(f"Instance {i} does not exists")
	exit()

# Now add tag to given instances
client.create_tags(Resources=instances_ids, Tags=[{"Key": tag_name, "Value": tag_value}])
for i in instances_names:
	print(f"Tag {tag_name}:{tag_value} added to {i}")
