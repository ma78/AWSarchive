# Import the SDK
import time
import boto
import uuid
from boto.ec2.connection import EC2Connection
from boto.sts import STSConnection
from sys import argv

script_name, account_id_from_user, role_name_from_user, my_region = argv

theregion = boto.ec2.get_region(my_region)

role_arn = "arn:aws:iam::" + account_id_from_user + ":role/"
role_arn += role_name_from_user

sts_connection = STSConnection()
assumed_role_object = sts_connection.assume_role(
        role_arn=role_arn,
        role_session_name="AssumeRoleSession"
        )
access = assumed_role_object.credentials.access_key
secret = assumed_role_object.credentials.secret_key
token = assumed_role_object.credentials.session_token

conn = EC2Connection(region=theregion)
ec2conn = EC2Connection(aws_access_key_id=access,aws_secret_access_key=secret,security_token=token,region=theregion)

listsnaps = conn.get_all_snapshots(owner='self')

for x in listsnaps:
        thesnap = str([x])
        thesnap =  thesnap.replace('Snapshot:','')
        thesnap = thesnap.replace('[','')
        thesnap = thesnap.replace(']','')
   print thesnap
        conn.modify_snapshot_attribute(thesnap, attribute='createVolumePermission', operation='add', user_ids=account_id_from_user)
        ec2conn.copy_snapshot('us-east-1',thesnap)
        time.sleep(30)

for x in listsnaps:
        thesnap = str([x])
        thesnap =  thesnap.replace('Snapshot:','')
        thesnap = thesnap.replace('[','')
        thesnap = thesnap.replace(']','')
        conn.modify_snapshot_attribute(thesnap, attribute='createVolumePermission', operation='remove', user_ids=account_id_from_user)
