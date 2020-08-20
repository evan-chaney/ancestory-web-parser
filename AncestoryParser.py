from bs4 import BeautifulSoup
import os
import re
import argparse

class Person:
    birthPlace: str
    deathPlace: str

    def __init__(self, person_id):
        self.id = int(person_id)
        self.name = None
        self.relations = []
        self.birthDate = ''
        self.birthPlace = ''
        self.deathDate = ''
        self.deathPlace = ''


class Relation:
    def __init__(self, person_id):
        #ID of other Person
        self.id = person_id
        #Type of Relation (e.g. brother, mother, etc)
        self.relation = None


def process_args():
    parser = argparse.ArgumentParser(description='Process a download of an geneology.com user website.')
    parser.add_argument('--web-root', '-r', type=str, action='append', dest='web_roots',
                        help="The directory where all your user pages were downloaded to")
    return parser.parse_args()



def process_file(file_contents, file_id):
    soup = BeautifulSoup(file_contents, 'html.parser')

    # Name
    person_name = str(soup.body.main.div.b)
    person_name = person_name.strip('<b/>')

    # Init object
    p = Person(file_id)
    p.name = person_name

    # Birth date and place
    person_birth_date_search = re.search('born\s+([\d\w]{2,15})\s+in\s+([\w\s,.]{2,20})\s+(and)\s+died\s+([\d\w]{2,15})\s+in\s+([\w\s,]{2,30}).', soup.body.main.div.text)
    if person_birth_date_search is not None:
        p.birthDate = str(person_birth_date_search.group(1))
        p.birthPlace = str(person_birth_date_search.group(2)).strip(',')
        p.deathDate = str(person_birth_date_search.group(4))
        p.deathPlace = str(person_birth_date_search.group(5))

    return p

#todo: make function to check all relations and make sure they exist


def transform_name(name):
    '''Transform a name into the proper format for writing to GEDCOM'''
    return re.sub(' ', ' /', name)


def generate_GEDCOM(person_list):
    output_file = open('output.ged', 'w')
    output_string = '''0 HEAD
1 SOUR PAF
2 NAME Ancestry Online
2 VERS 5.5.1
1 DATE 25 DEC 2018
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR ANSEL
1 SUBM @U1@
'''
    for _person in person_list:
        print(_person.name, _person.id, _person.birthDate, _person.birthPlace,_person.deathDate, _person.deathPlace)
        output_string += "0 @I" + str(_person.id) + "@ INDI\n"
        output_string += "1 NAME " + str(transform_name(_person.name)) + '/\n'
    output_string += '''0 @U1@ SUBM
1 NAME Submitter
0 TRLR'''

    output_file.write(output_string)
    output_file.close()


personList = []

args = process_args()
for web_dir in args.web_roots:
    for f in os.listdir(web_dir):
        personID = f.split('-')[1].split('.')[0]
        if personID.isnumeric():
            retObj = process_file(open(web_dir + '/' + f).read(), personID)
            if retObj is not None:
                personList.append(retObj)

generate_GEDCOM(personList)
#for Person in person_list:
#    print(Person.name,Person.person_id)

