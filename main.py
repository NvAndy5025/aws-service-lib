import boto3
import assumeRole

response = assumeRole.assume_role_with_web_identity("arn:aws:iam::946096813098:role/anisnewrole","aniSession")