import pulumi
import pulumi_aws as aws
from assumeRole import assume_role_with_web_identity
import asyncio
import os
from pulumi.automation import LocalWorkspace, create_or_select_stack, LocalWorkspaceOptions, OutputMap
import sys
import json
import pulumi
from pulumi import automation as auto
from pulumi_aws import s3
import boto3
from botocore.credentials import AssumeRoleWithWebIdentityCredentialFetcher
import time


def deploy_ec2(roleArn, sessionName,region):
    credentials = assume_role_with_web_identity(roleArn, sessionName)

    stsClient = boto3.client("ec2",aws_access_key_id=credentials['aws_access_key_id'],
                             aws_secret_access_key=credentials['aws_secret_access_key'],
                             aws_session_token=credentials['aws_session_token'],
                             region_name=region)

    response = stsClient.run_instances(
        ImageId='ami-01572eda7c4411960',
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        IamInstanceProfile={'Name': 'ani_role'})
    
    instance_id = response['Instances'][0]['InstanceId']
    print(instance_id)

    session = boto3.Session(
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'],
        aws_session_token=credentials['aws_session_token'],
        region_name=region)
    
    ec2_instance_resource = session.resource('ec2').Instance(instance_id)
    ec2_instance_resource.wait_until_running()
    ec2_instance_resource.reload()

    # Install Docker using SSM
    ssm_client = session.client('ssm', region_name=region)

    commands = [
        "sudo yum update -y",
        "sudo yum install -y cmake"
    ]

    # Send command to install Docker
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': commands}
    )
    
    command_id = response['Command']['CommandId']

    print("Sleeping for few seconds...")
    time.sleep(35)

    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )

    if output['Status'] == 'Success':
        return "Cmake installation successful on Instance with ID:" + instance_id 
    else:
        print("Cmake installation failed")
        return "Cmake installation failed on Instance with ID:" + instance_id 