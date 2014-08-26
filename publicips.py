import boto.ec2

# Script to print out all public IP addressing in use across all regions

print "Spare EIPs"
theregionlist = [region.name for region in boto.ec2.regions() if region.name not in ['us-gov-west-1', 'cn-north-1']]
for region in theregionlist:
        conn = boto.ec2.connect_to_region(region)
        print region

        myeip = conn.get_all_addresses()
        for x in myeip:
                print x.public_ip

        listofrevs = conn.get_all_instances()
        for r in listofrevs:
                for i in r.instances:
                        print i.ip_address
                        # print i.tags['Name']
