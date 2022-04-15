#! /usr/env python3
import boto3
import argparse

# Add needed arguments
parser = argparse.ArgumentParser()
parser.add_argument("--tag-name", "-tn", help="Tag Name")
parser.add_argument("--tag-value", "-tv", help="Tag Value")
parser.add_argument("--authorize", "-a", nargs="?", const=True, default=False, help="Authorize security group access")
parser.add_argument("--revoke", "-r", nargs="?", const=True, default=False, help="Revoke security group access")
parser.add_argument("--port", "-p", type=int, help="Specify Port")
parser.add_argument("--inbound", "-i", nargs="?", const=True, default=False, help="Specify inbound access")
parser.add_argument("--outbound", "-o", nargs="?", const=True, default=False, help="Specify outbound access")

# Get args
tag_name = parser.parse_args().tag_name
tag_value = parser.parse_args().tag_value
authorize = parser.parse_args().authorize
revoke = parser.parse_args().revoke
port = parser.parse_args().port
inbound = parser.parse_args().inbound
outbound = parser.parse_args().outbound

# Authorize vs revoke
if authorize is True and revoke is True:
	print("You must choose between authorize and revoke")
	exit()
elif authorize is False and revoke is False:
	print("You must choose authorize or revoke")
	exit()

# Get all instances filtered by tag
client = boto3.client("ec2")
filters = [{"Name": f"tag:{tag_name}", "Values": [tag_value]}]
response = client.describe_instances(Filters=filters)

# Get security groups ids of each instances
security_group_ids = []
for instance in response["Reservations"][0]["Instances"]:
	for group in instance["SecurityGroups"]:
		security_group_ids.append(group["GroupId"])

# Set rules on all security groups by their ids
ip_permissions = [{"FromPort": port, "IpProtocol": "tcp", "ToPort": port, "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]
for security_group_id in security_group_ids:
	if authorize:
		if inbound:
			client.authorize_security_group_ingress(GroupId=security_group_id, IpPermissions=ip_permissions)
		if outbound:
			client.authorize_security_group_egress(GroupId=security_group_id, IpPermissions=ip_permissions)
	else:
		if inbound:
			client.revoke_security_group_ingress(GroupId=security_group_id, IpPermissions=ip_permissions)
		if outbound:
			client.revoke_security_group_egress(GroupId=security_group_id, IpPermissions=ip_permissions)

# Return print
print(f"Security groups {' '.join(security_group_ids)} now {'authorize' if authorize else 'revoke'} "
      f"traffic on port {port} with inbound={inbound} and outbound={outbound}")
