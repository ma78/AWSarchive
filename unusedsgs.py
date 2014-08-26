import boto.ec2

# Script to print out all public IP addressing in use across all regions

print "unused SGs"
theregionlist = [region.name for region in boto.ec2.regions() if region.name not in ['us-gov-west-1', 'cn-north-1']]

for region in theregionlist:
        conn = boto.ec2.connect_to_region(region)
        print region

# create a list of all security groups by name
        all_groups = conn.get_all_security_groups()
# create a list containing all instance IDs
        all_instances = conn.get_only_instances()

        fulllist = []
        for m in all_groups:
                fulllist.append(m.id)
        
        ec2list = []
        for x in all_instances:
                for i in x.groups:
                        ec2list.append(i.id)
        
        unused = [a for a in fulllist if a not in ec2list]
        print unused
