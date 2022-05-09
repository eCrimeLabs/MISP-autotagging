#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymisp import ExpandedPyMISP
from pymisp import PyMISP
from datetime import tzinfo, timedelta, datetime, timezone
import argparse
import re
import json
import pprint
import sys
from collections import defaultdict
from config import misp_url, misp_key, misp_verifycert, search_template, dict_orgtags

def timestamp():
    return(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z - "))

def search_add_misp(misp, org, time):
    search_query = search_template
    search_query['org'] = org
    search_query['publish_timestamp'] = time
    events = {}
    response_lists = misp.direct_call('/events/restSearch', search_query)
    for response in response_lists:
        if response['Event']['Orgc']['uuid'] == org:
            event_uuid = response['Event']['uuid']
            add_tags = dict_orgtags[org]
            if 'Tag' in response['Event'].keys():
                for tag in response['Event']['Tag']:
                    tag_name = tag['name']
                    if tag_name in add_tags:
                        add_tags.remove(tag_name)
            else:
                pass
            events[event_uuid] = add_tags
    return(events)

def search_remove_misp(misp, org, time):
    events = defaultdict(list)
    for tag in dict_orgtags[org]:
        search_query = search_template
        search_query['org'] = org
        search_query['publish_timestamp'] = time
        search_query['tag'] = tag
        response_lists = misp.direct_call('/events/restSearch', search_query)
        for response in response_lists:
            if response['Event']['Orgc']['uuid'] == org:
                for find_tag in response['Event']['Tag']:
                    if (find_tag['name'] == tag and find_tag['local'] == 1):
                        event_uuid = response['Event']['uuid']
                        events[event_uuid].append(tag)
    return(events)


def misp_add_tags(pymisp, events):
    for event in events:
        for tag in events[event]:
            add_tag = pymisp.tag(event, tag, local=True)
            if(add_tag['success'] and add_tag['saved']):
                print (timestamp() + "Successfully added local tag: " + tag + " to Event UUID: " + event)
            else:
                print (timestamp() + "FAILED added local tag: " + tag + " to Event UUID: " + event)


def misp_remove_tags(pymisp, events):
    for event in events:
        for tag in events[event]:
            add_tag = pymisp.untag(event, tag)
            if(add_tag['success'] and add_tag['saved']):
                print (timestamp() + "Successfully removed local tag: " + tag + " from Event UUID: " + event)
            else:
                print (timestamp() + "FAILED removed local tag: " + tag + " from Event UUID: " + event)


def perform_task(task, time):
    # task: True = add, False = remove
    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)
    pymisp = PyMISP(misp_url, misp_key, misp_verifycert, 'json')
    for dict_orgtag in dict_orgtags:
        if(task):
            events_for_update = search_add_misp(misp, dict_orgtag, time)
        else:
            events_for_update = search_remove_misp(misp, dict_orgtag, time)

        if (events_for_update and task):
            # Add tags to event
            misp_add_tags(pymisp, events_for_update)
        elif (events_for_update and not task):
            # Remove tags from events
            misp_remove_tags(pymisp, events_for_update)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", action='store_true', help="Add local tags to Event(s)")
    parser.add_argument("-r", "--remove", action='store_true', help="Remove local tags to Event(s)")
    parser.add_argument("-d", "--days", type=str, default="2", help="Number of days to look back for events (Default: 2)")
    args = parser.parse_args()

    if not re.fullmatch("^[0-9]{1,4}$", args.days, re.MULTILINE):
        print ('Number of days has to be between "1" and "9999"')
        parser.print_help()
        sys.exit(2)
    if (args.add):
        print ("Add local tags to Event(s)")
        perform_task(True, args.days + 'd')
    elif (args.remove):
        print ("Remove local tags to Event(s)")
        perform_task(False, args.days + 'd')
    else:
        parser.print_help()
        sys.exit(2)
