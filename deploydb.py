import argparse
from datetime import datetime
import logging
import json
import sys

import boto3
import botocore


def run(args):
    region = 'ap-south-1'
    cf = boto3.client('cloudformation', aws_access_key_id=args.access_key, aws_secret_access_key=args.secret_key, region_name=region)

    template_data = _parse_template(cf, args.template)

    parameter_data = [
        {"ParameterKey": "userIndexName", "ParameterValue": "user-city-index"},
        {"ParameterKey": "userTableName", "ParameterValue": 'myapp.User'},
    ]

    stack_name = args.stack_name

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Parameters': parameter_data,
    }

    try:
        if _stack_exists(cf, stack_name):
            print('Updating {}'.format(stack_name))
            stack_result = cf.update_stack(**params)
            waiter = cf.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            stack_result = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise
    else:
        print(json.dumps(
            cf.describe_stacks(StackName=stack_result['StackId']),
            indent=2,
            default=json_serial
        ))



def _parse_template(cf, template):
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf.validate_template(TemplateBody=template_data)
    return template_data


def _parse_parameters(cf, parameters):
    with open(parameters) as parameter_fileobj:
        parameter_data = json.load(parameter_fileobj)
    return parameter_data


def _stack_exists(cf, stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


def main():
    p = argparse.ArgumentParser(description='create or update stack')
    p.add_argument("--access_key", "--access_key", required=True, help="aws access key")
    p.add_argument("--secret_key", "--secret_key", required=True, help="aws secret key")
    p.add_argument("--stack_name", "--stack_name", required=True, help="stack name")
    p.add_argument("--template", "--template", required=True, help="cf template name")

    args = p.parse_args()

    log = logging.getLogger('deploy.cf.create_or_update')  # pylint: disable=C0103

    run(args)

main()
