import boto3
import time

from app.assumeRole import assume_role_with_web_identity

def installDockerOnInstance(instanceId,region,roleArn):

    credentials = assume_role_with_web_identity(roleArn, "docker")

    session = boto3.Session(
        aws_access_key_id=credentials['aws_access_key_id'],
        aws_secret_access_key=credentials['aws_secret_access_key'],
        aws_session_token=credentials['aws_session_token'],
        region_name=region)
    
    # Install Docker using SSM
    ssm_client = session.client('ssm', region_name=region)

    commands = [
        "sudo yum update -y",
        "sudo yum install -y docker",
        "sudo service docker start",
        "sudo usermod -aG docker ec2-user",
        "docker --version"
    ]

    # Send command to install Docker
    response = ssm_client.send_command(
        InstanceIds=[instanceId],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': commands}
    )

    command_id = response['Command']['CommandId']

    # Check command status
    time.sleep(10)  # Wait a few seconds before checking the status

    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instanceId,
    )

    if output['Status'] == 'Success':
        print("Docker installation successful")
        print("Output:\n", output['StandardOutputContent'])
    else:
        print("Docker installation failed")
        print("Error:\n", output['StandardErrorContent'])
    
