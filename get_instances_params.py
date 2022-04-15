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

# Now filter the result to get few information about each instance and print them
print(f"Instances found with tag {tag_name}:{tag_value} \n")
for instance in response["Reservations"][0]["Instances"]:
	print({
		"image_id": instance["ImageId"],
		"instance_id": instance["InstanceId"],
		"instance_type": instance["InstanceType"],
		"availability_zone": instance["Placement"]["AvailabilityZone"],
		"tags": instance["Tags"]
	})
	print("\n")
