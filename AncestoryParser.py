from bs4 import BeautifulSoup
import os
import re


class Person:
    def __init__(self, id):
        self.id = int(id)
        self.name = None
        self.relations = []
        self.city = None
        self.birthDate = None
        self.deathDate = None


class Relation:
    def __init__(self, id):
        #ID of other Person
        self.id = id
        #Type of Relation (e.g. brother, mother, etc)
        self.relation = None


def process_file(file_contents, file_id):
    soup = BeautifulSoup(file_contents, 'html.parser')
    name = str(soup.body.main.div.b)
    name = name.strip('<b/>')

    p = Person(id)
    p.name = name

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
        print(_person.name, _person.id)
        output_string += "0 @I" + str(_person.id) + "@ INDI\n"
        output_string += "1 NAME " + str(transform_name(_person.name)) + '/\n'
    output_string += '''0 @U1@ SUBM
1 NAME Submitter
0 TRLR'''

    output_file.write(output_string)
    output_file.close()


personList = []

for f in os.listdir(''):
    personID = f.split('-')[1].split('.')[0]
    if personID.isnumeric():
        retObj = process_file(open('' + f).read(), personID)
        if retObj is not None:
            personList.append(retObj)

generate_GEDCOM(personList)
#for Person in person_list:
#    print(Person.name,Person.id)

