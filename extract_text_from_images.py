#! /usr/env python3
import boto3
import os
import argparse

# Add image path params
parser = argparse.ArgumentParser()
parser.add_argument("--folder", "-f", help="Absolute folder path which contains images")
folder = parser.parse_args().folder

# Check if folder exists
if not os.path.exists(folder):
	print(f"{folder} does not exists")
	exit()

# Check if all images format are supported by textract
images = os.listdir(folder)
supported_formats = [".pdf", ".tiff", ".jpg", ".jpeg", ".png"]
not_supported = False
for image in images:
	format = os.path.splitext(image)[1]
	if format not in supported_formats:
		not_supported = True
		print(f"Image {image} with format {format} is not supported, use {' '.join(supported_formats)} instead")
if not_supported:
	exit()

# Extract text from images
client = boto3.client("textract")
results = []
for image in images:
	with open(f"{folder}/{image}", "rb") as file:
		img = bytearray(file.read())
	response = client.detect_document_text(Document={"Bytes": img})
	text = [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]
	results.append([image, text])

# Print results
for result in results:
	print(f"Image: {result[0]}, detected text: {result[1]}")
