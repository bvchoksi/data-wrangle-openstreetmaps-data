"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "mumbai_india.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Road", "Marg", "Drive", "Lane", "Highway", "Chawl", "Galli", "Path"]

# UPDATE THIS VARIABLE
#If I did not encounter an expected street type in any form, I have left it out of the mapping
#I have updated this variable based on observation of the audit output
mapping = { "st" : "Street",
			"ROAD" : "Road", "ROad" : "Road", "Raod" : "Road", "Rd" : "Road", "Rd." : "Road",
            "marg" : "Marg",
            "lane" : "Lane",
            "chawl" : "Chawl",
            "Gali" : "Galli", "galli" : "Galli"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(element):
    return (element.attrib['k'] == "addr:street")


#The following function returns unique street types
#in "v" attribute of tags where k = "addr:street"
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    for _, element in ET.iterparse(osm_file, events=("start",)):
		if element.tag == "node" or element.tag == "way":
			for tag in element.iter("tag"):
				if is_street_name(tag):
					audit_street_type(street_types, tag.attrib['v'])
    
    return street_types


#The following function cleans up the street names
#based on the correct street types set up in the
#mapping dictionary
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = street_type_re.sub(mapping[street_type], name)
    
    return name


if __name__ == '__main__':
    st_types = audit(OSMFILE)
    print len(st_types), "Street Types:"
    pprint.pprint(dict(st_types))
    
    print "\nBetter Names:"
    for st_type, ways in st_types.iteritems():
        for name in ways:
        	better_name = update_name(name, mapping)
        	if better_name != name:
        		print name, "=>", better_name