import json
import boto3
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

import requests

client = boto3.client('cloudfront')


def handler(event, context):
    custom_resource_response_base = {
        'Reason': 'See the details in CloudWatch Logs: {} - {}'.format(context.log_group_name, context.log_stream_name),
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId']
    }

    cloudfront_origin_access_identity_config = event['ResourceProperties']['CloudFrontOriginAccessIdentityConfig']

    try:
        if event['RequestType'] == 'Create':
            response = client.create_cloud_front_origin_access_identity(
                CloudFrontOriginAccessIdentityConfig={
                    'CallerReference': cloudfront_origin_access_identity_config['CallerReference'],
                    'Comment': cloudfront_origin_access_identity_config['Comment']
                }
            )

            physical_resource_id = response['CloudFrontOriginAccessIdentity']['Id']

            custom_resource_response = custom_resource_response_base
            custom_resource_response['PhysicalResourceId'] = physical_resource_id
            custom_resource_response['Status'] = 'SUCCESS'
            custom_resource_response['Data'] = {'Id': physical_resource_id}

        elif event['RequestType'] == 'Update':
            physical_resource_id = event['PhysicalResourceId']

            get_cloudfront_origin_qccess_identity_result = client.get_cloud_front_origin_access_identity(
                Id=physical_resource_id
            )

            response = client.update_cloud_front_origin_access_identity(
                CloudFrontOriginAccessIdentityConfig={
                    'CallerReference': get_cloudfront_origin_qccess_identity_result['CloudFrontOriginAccessIdentity']['CloudFrontOriginAccessIdentityConfig']['CallerReference'],
                    'Comment': event['ResourceProperties']['CloudFrontOriginAccessIdentityConfig']['Comment']
                },
                Id=physical_resource_id,
                IfMatch=get_cloudfront_origin_qccess_identity_result['ETag']
            )
            custom_resource_response = custom_resource_response_base
            custom_resource_response['PhysicalResourceId'] = physical_resource_id
            custom_resource_response['Status'] = 'SUCCESS'
            custom_resource_response['Data'] = {'Id': physical_resource_id}

        elif event['RequestType'] == 'Delete':
            physical_resource_id = event['PhysicalResourceId']

            get_cloudfront_origin_qccess_identity_result = client.get_cloud_front_origin_access_identity(
                Id=physical_resource_id
            )

            response = client.delete_cloud_front_origin_access_identity(
                Id=physical_resource_id,
                IfMatch=get_cloudfront_origin_qccess_identity_result['ETag']
            )

            custom_resource_response = custom_resource_response_base
            custom_resource_response['PhysicalResourceId'] = physical_resource_id
            custom_resource_response['Status'] = 'SUCCESS'
            custom_resource_response['Data'] = {}

    except Exception as e:
        if event['RequestType'] == 'Create':
            physical_resource_id = ''
        else:
            physical_resource_id = event['PhysicalResourceId']

        custom_resource_response = custom_resource_response_base
        custom_resource_response['Status'] = 'FAILED'
        custom_resource_response['PhysicalResourceId'] = physical_resource_id
        custom_resource_response['Data'] = {'Error': str(e)}

    response_url = event['ResponseURL']
    print('custom_resource_response:')
    print(custom_resource_response)

    headers = {'Content-Type': ''}
    custom_resource_response_put_result = requests.put(response_url, data=json.dumps(custom_resource_response), headers=headers)

    return custom_resource_response

