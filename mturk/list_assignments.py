#!/usr/bin/env python3
import re
import json
import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--hit_id", required=True, type=str)
parser.add_argument("-p", "--prod", required=False, action="store_true")
args = parser.parse_args()

if args.prod:
    endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"
else:
    endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"

client = boto3.client('mturk', endpoint_url=endpoint_url)

def parse_response(response):
    results = []
    for assignment_ in response["Assignments"]:
        answers = assignment_["Answer"]
        assignment = {}
        assignment["assignment_id"] = assignment_["AssignmentId"]
        assignment["hit_id"] = assignment_["HITId"]
        assignment["worker_id"] = assignment_["WorkerId"]
        assignment["accept_time"] = assignment_["AcceptTime"].timestamp() # ms since epoch
        assignment["submit_time"] = assignment_["SubmitTime"].timestamp() # ms since epoch
        if "$$$" not in answers:
            results.append(assignment)
            continue
        assignment["answers"] = json.loads(re.search(r"\$\$\$(.*)\$\$\$", answers).group(1))
        results.append(assignment)
    return results

response = client.list_assignments_for_hit(
    HITId=args.hit_id
)

print(json.dumps(parse_response(response)))
