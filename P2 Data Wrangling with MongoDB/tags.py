#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
	if element.tag == "tag":
		if lower.search(element.attrib["k"]):
			keys["lower"] += 1
		elif lower_colon.search(element.attrib["k"]):
			if element.attrib["k"] in keys["lower_colon"]:
				keys["lower_colon"][element.attrib["k"]] += 1
			else:
				keys["lower_colon"][element.attrib["k"]] = 1
		elif problemchars.search(element.attrib["k"]):
			if element.attrib["k"] in keys["problemchars"]:
				keys["problemchars"][element.attrib["k"]] += 1
			else:
				keys["problemchars"][element.attrib["k"]] = 1
		else:
			if element.attrib["k"] in keys["other"]:
				keys["other"][element.attrib["k"]] += 1
			else:
				keys["other"][element.attrib["k"]] = 1
	
	return keys
    

def process_map(filename):
    keys = {"lower": 0, "lower_colon": {}, "problemchars": {}, "other": {}}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys


if __name__ == "__main__":
    keys = process_map('mumbai_india.osm')
    pprint.pprint(keys)