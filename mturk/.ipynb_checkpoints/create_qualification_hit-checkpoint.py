#!/usr/bin/env python3
import boto3
import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="File with 1 URL row per line.")
    parser.add_argument("-t", "--template", required=True, help="Template defining the HIT.")
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
    links = open(args.input).readlines()
    indices = list(range(1, len(links) + 1))
    
    link_template = '<div><a href="{}" target="_blank">Link {}</a><input type="text" id="link{}" style="width: 600px;"></div>'
    links = [link_template.format(link, i+1, i+1) for i, link in enumerate(links)]
    answers = ['answer.link{} = $("#link{}").val();'.format(i,i) for i in indices]

    template = template.replace("===LINKS===", "\n".join(links))
    template = template.replace("===ANSWERS===", "\n".join(answers))
    template = template.replace("===NUMLINKS===", str(len(links)))

    response = client.create_hit(
        MaxAssignments=20,
        AutoApprovalDelayInSeconds=2592000,
        LifetimeInSeconds=31536000,
        AssignmentDurationInSeconds=2000,
        Reward='0.10',
        Title='Finding gas prices in Street View Imagery (qualification)',
        Keywords='vision,copy-paste,easy,computer vision',
        Description='Help us find gas prices in Street View Imagery. There will be many HITs for workers who qualify.',
        Question=template,
        RequesterAnnotation='something',
        QualificationRequirements=[
        # at least 95% of assignments were approved
        {
            'QualificationTypeId': '000000000000000000L0',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [
                95,
            ],
            
        },
        # submitted at least 200 assignments
        {
            'QualificationTypeId': '00000000000000000040',
            'Comparator': 'GreaterThanOrEqualTo',
            'IntegerValues': [
                200,
            ],
        }
        ] 
    )

    hit_id = response["HIT"]["HITId"]

    if args.output:
        with open(args.output, "a") as output_file:
            output_file.write(f"{hit_id}\n")
    
    print(hit_id)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
