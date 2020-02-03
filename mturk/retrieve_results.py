#!/usr/bin/env python3
import boto3
import sys
import json
import re
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", dest="prod", action="store_true", help="Whether the HIT is in the production environment.")
    parser.add_argument("-t", "--hitid", required=False, help="Hit ID.")
    parser.add_argument("-i", "--input_file", required=False, help="File with HIT Ids.")
    parser.add_argument("-o", "--output", help="Where the assignment should be saved.")
    return parser.parse_args()

def parse_response(response):
    answers = response["Assignments"][0]["Answer"]
    assignment = {}
    assignment["answers"] = json.loads(re.search(r"\$\$\$(.*)\$\$\$", answers).group(1))
    assignment["assignment_id"] = response["Assignments"][0]["AssignmentId"]
    assignment["hit_id"] = response["Assignments"][0]["HITId"]
    assignment["worker_id"] = response["Assignments"][0]["WorkerId"]
    assignment["accept_time"] = response["Assignments"][0]["AcceptTime"].timestamp() # ms since epoch
    assignment["submit_time"] = response["Assignments"][0]["SubmitTime"].timestamp() # ms since epoch
    return assignment


def main(args):

    endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
    if args.prod:
        endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"

    client = boto3.client('mturk', endpoint_url=endpoint_url)

    if args.hitid:
        # Retrieve hits
        response = client.list_assignments_for_hit(HITId=args.hitid)
        try:
            assignment = parse_response(response)
        except:
            assignment = {}
        print(json.dumps(assignment, indent=4))
        return

    if args.input_file:
        hit_ids = [hit_id.rstrip("\n") for hit_id in open(args.input_file)]
        assignments = []
        for hit_id in hit_ids:
            response = client.list_assignments_for_hit(HITId=hit_id)
            try:
                assignment = parse_response(response)
            except:
                assignment = {}
            assignments.append(assignment)
        print(json.dumps(assignments, indent=4))

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
