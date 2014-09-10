import boto.ec2
import boto.ec2.elb
import socket


theregionlist = [region.name for region in boto.ec2.regions() if region.name not in ['us-gov-west-1','cn-north-1']]
listofips = []

for ec2region in theregionlist:
    #Make a connection to the regional EC2 endpoint with access/secret key specified
    makeconn = boto.ec2.connect_to_region(ec2region,aws_access_key_id=access, aws_secret_access_key=secret)
    # Print out all EIPs in use
    listofips.append([y.public_ip for y in makeconn.get_all_addresses()])
    # Instances started in VPCs might have public IP addresses attached which aren't EIPs
    listofips.append([t.ip_address for t in makeconn.get_only_instances()])

for elbregion in theregionlist:
    #Make a Connection to regional ELB endpoint with access/secret key specified
    elbconn = boto.ec2.elb.connect_to_region(elbregion,aws_access_key_id=access, aws_secret_access_key=secret)
    # Print out IP addresses for the CNAMEs of the ELBs
    listofips.append([j.canonical_hosted_zone_name for j in elbconn.get_all_load_balancers()])
    
print listofips

