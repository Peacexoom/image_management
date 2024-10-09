# import boto3 

# aws_management_console = boto3.session.Session() 
# ec2_console = aws_management_console.client('ec2') 

# response = ec2_console.create_instances( 
#     ImageId="ami-097c5c21a18dc59ea",
#     InstanceType='t2.micro', 
#     MaxCount=1, 
#     MinCount=1
# )

import boto3

def create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-1")

    instances = ec2_client.run_instances(
        ImageId="ami-097c5c21a18dc59ea",
        MinCount=1,
        MaxCount=1,
        InstanceType="t3.micro",
    )

    print(f'The instance launched with ID: {instances["Instances"][0]["InstanceId"]}')

if __name__ == "__main__":
    create_instance()