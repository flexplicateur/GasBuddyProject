import re
import json
import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--hit_id", required=True, type=str)
parser.add_argument("-p", "--prod", required=False, action="store_true")
args = parser.parse_args()

if args.prod:
    endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
else:
    endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"
    
client = boto3.client('mturk', endpoint_url=endpoint_url)

def parse_response(response):
    results = []
    for assignment_ in response["Assignments"]:
        answers = assignment_["Answer"]
        assignment = {}
        assignment["answers"] = json.loads(re.search(r"\$\$\$(.*)\$\$\$", answers).group(1))
        assignment["assignment_id"] = response["Assignments"][0]["AssignmentId"]
        assignment["hit_id"] = response["Assignments"][0]["HITId"]
        assignment["worker_id"] = response["Assignments"][0]["WorkerId"]
        assignment["accept_time"] = response["Assignments"][0]["AcceptTime"].timestamp() # ms since epoch
        assignment["submit_time"] = response["Assignments"][0]["SubmitTime"].timestamp() # ms since epoch
        results.append(assignment)
    return results

response = client.list_assignments_for_hit(
    HITId=args.hit_id
)

print(parse_response(response))