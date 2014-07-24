# Import the SDK
import boto
import uuid
import boto.ec2
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

myimages = EC2Connection(region=theregion)
listims = myimages.get_all_images(owners='self')
ec2conn = EC2Connection(aws_access_key_id=access,aws_secret_access_key=secret,security_token=token,region=theregion)

for x in listims:
        theimage = str([x])
        theimage = theimage.replace('Image:','')
        theimage = theimage.replace('[','')
        theimage = theimage.replace(']','')
 myimages.modify_image_attribute(theimage, attribute='launchPermission', operation='add', user_ids=account_id_from_user)
        launchit = ec2conn.run_instances(theimage, max_count=1,instance_type='t2.micro',)
        print launchit

        # myimages.modify_image_attribute(theimage, attribute='launchPermission', operation='remove', user_ids=account_id_from_user)
