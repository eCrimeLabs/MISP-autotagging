#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymisp import ExpandedPyMISP
from pymisp import PyMISP
from datetime import tzinfo, timedelta, datetime, timezone
import json
import pprint
from config import misp_url, misp_key, misp_verifycert, search_time, search_template, dict_orgtags

def timestamp():
    return(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z - "))

def search_misp(org):
    search_query = search_template
    search_query['org'] = org
    events = {}
    response_lists = pymisp.direct_call('/events/restSearch', search_query)
    for response in response_lists:
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

def misp_add_tags(events):
    for event in events:
        for tag in events[event]:
            add_tag = pymisp.tag(event, tag, local=True)
            if(add_tag['success'] and add_tag['saved']):
                print (timestamp() + "Successfully added local tag: " + tag + " to Event UUID: " + event)
            else:
                print (timestamp() + "FAILED added local tag: " + tag + " to Event UUID: " + event)

if __name__ == '__main__':
    misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert)
    pymisp = PyMISP(misp_url, misp_key, misp_verifycert, 'json')
    for dict_orgtag in dict_orgtags:
        events_for_update = search_misp(dict_orgtag)
        if events_for_update:
            misp_add_tags(events_for_update)
