import boto3
import generateToken

def assume_role_with_web_identity(roleArn, sessionName):
  
  # Create an STS client
  sts_client = boto3.client('sts')
  
  #generates web-identity token
  identity_token = generateToken.get_token()

  # Assume the role with web identity
  response = sts_client.assume_role_with_web_identity(
    RoleArn = roleArn,
    RoleSessionName=sessionName,
    WebIdentityToken= identity_token
    )
  # Extract temporary credentials
  credentials = response['Credentials']

  return {
      'aws_access_key_id': credentials['AccessKeyId'],
      'aws_secret_access_key': credentials['SecretAccessKey'],
      'aws_session_token': credentials['SessionToken']
  }
