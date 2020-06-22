#this program or scripts fetches IAM users and stores it in CSV file
import boto3
import csv

from datetime import date, datetime, timedelta, timezone

client = boto3.client('iam', aws_access_key_id="AKIATKQXWGYZORI4MN5K",
                      aws_secret_access_key="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")


def access_key(writer):
    key_details = {}

    list_user = client.list_users()

    for users in list_user['Users']:
        access_key = client.list_access_keys(UserName=users['UserName'])
        for details in access_key['AccessKeyMetadata']:
            current_date = datetime.now(timezone.utc)
            age = (current_date - details['CreateDate']).days
            if age >= 0:
                key_details["UserName"] = details['UserName']
                key_details["AccessKeyId"] = details['AccessKeyId']
                key_details["Created_date"] = details['CreateDate']
                key_details["key_age"] = str(age)
                print(key_details)
                writer.writerow(key_details)


def main():
    fieldnames = ["UserName", "AccessKeyId", "Created_date", "key_age"]
    file_name = "key_details.csv"
    with open(file_name, "w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        access_key(writer)


main()