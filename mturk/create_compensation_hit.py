#!/usr/bin/env python3
import boto3
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="File with workers to compensate.")
    parser.add_argument("-t", "--template", required=True, help="Compensation template.")
    parser.add_argument("-p", "--production", action="store_true", help="Whether to launch the HIT in production.")
    parser.add_argument("-o", "--output", help="Where the response (with HIT ID) should be saved.")
    return parser.parse_args()

def main(args):
    if args.production:
        endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"
    else:
        endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"

    client = boto3.client('mturk', endpoint_url=endpoint_url)

    template = open(args.template).read()

    # Create a qual for the workers
    for worker in open(args.input).readlines():
        response = client.associate_qualification_with_worker(
            QualificationTypeId='326R1R7QAAXHZLZTJQCW3NNXJIIBXU',
            WorkerId=worker.rstrip("\n"),
            IntegerValue=123,
            SendNotification=False
        )
        print(response)

    response = client.create_hit(
        MaxAssignments=len(open(args.input).readlines()),
        AutoApprovalDelayInSeconds=2592000,
        LifetimeInSeconds=31536000,
        AssignmentDurationInSeconds=1800,
        Reward='0.01',
        Title='Compensation',
        Keywords='compensation',
        Description='Complete the HIT so that I can send a bonus.',
        Question=template,
        RequesterAnnotation='something',
        QualificationRequirements=[
        # at least 95% of assignments were approved
        {
            'QualificationTypeId': '326R1R7QAAXHZLZTJQCW3NNXJIIBXU',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [123],
            'ActionsGuarded': 'DiscoverPreviewAndAccept'
        },
        ] 
    )

    print(response)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
