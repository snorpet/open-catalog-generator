#!/usr/bin/python
# James Tobat, 2014
import csv
import os
import re
import copy

programName_template = "DARPA Program Name"
# Parses a csv document in a mode (pub, project, program)
# using a schema that it can attach JSON information to.
# The end result is an array of JSON information which includes
# the document title as well as all the JSON records identified
# in the document (all use the schema passed in)
def parse_csv(document, mode, schema, template):
  JSON_Information = []
  
  if not template:
    document = os.path.basename(document)
    # Uses the name of the document given but replaces the file type
    # with JSON. This will be the name of the output file.
    doc_name = re.sub(".csv", ".json", document, flags=re.I)
    JSON_Information.append(doc_name)
    # Identifies the DARPA Program by removing
    # the schema name from the file name e.g.
    # HACM-pubs would change to HACM.
    # Assumes the title of the document contains the 
    # DARPA Program's name either in the form
    # DARPA_Program-schema_type.filetype e.g. HACM-pubs.csv
    # or is the name of the file itself e.g. PPAML.csv
    darpa_program = re.sub("-.*","",document)
    darpa_program = re.sub("\..*","",darpa_program)
    schema['DARPA Program'] = darpa_program
    #print doc_name
  
  with open(document, 'r') as read_file:
    reader = csv.reader(read_file)
    # With the first row, checks the column titles given
    # in order to identify which column maps to which schema
    # item
    initial_row = True
    first_values = False
    team_index = -1
    title_index = -1
    link_index = -1
    project_index = -1
    category_index = -1
    code_index = -1
    home_index = -1
    description_index = -1
    license_index = -1

    template_fields = {} # stores row locations of JSON fields
    for row in reader:
      # Uses the schemas from the examples JSON file, this assumes
      # that the Excel columns have the same names as the JSON schema fields
      if template:
        # Checks if it one of the first rows
        if initial_row:
          # Checks to see if a header is present and ignores it
          header = re.search("Meta Data Fields", row[0], flags=re.I)
          # If it isn't the header, assumes the next rows are data 
          # for the JSON file
          if not header:
            initial_row = False
            k = 0
            first_values = True
            # Finds and stores the row index of each JSON field
            for column in row:
              template_fields[column] = k
              k += 1
        else:
          # This is only meant to be run once, as it finds the
          # DARPA Program Name and creates a file name from it
          # using the mode.
          darpa = ""
          if first_values:
            if mode == 'program':
              darpa = 'DARPA Program Name'
            else: 
              darpa = 'DARPA Program'
            index = template_fields[programName_template]
            program_name = row[index].strip()
            schema[darpa] = program_name
            file_name = program_name + '-' + mode + '.json'
            JSON_Information.append(file_name)
            first_values = False
          
          schema_copy = copy.deepcopy(schema) # Ensures that no wrong values are kept
          # Goes through each JSON field in the schema and finds its corresponding value
          for key, value in schema.iteritems():
            # Ensures that the DARPA Program Name is kept and that fields that
            # aren't present in the spreadsheet aren't being read in.
            if key != darpa and key in template_fields:
              index = template_fields[key]
              # Splits Excel cells that have comma separated values
              # into a list then trims each value of excess whitespace
              item_list = row[index].split(',')
              if isinstance(schema[key], list):
                new_list = []
                for item in item_list:
                  item = item.strip()
                  if item.endswith('.'):
                    item = item[:-1]
                  new_list.append(item)

                schema_copy[key] = new_list
              else:
                # Simply stores the value in the schema
                # if it isn't a list.
                schema_copy[key] = row[index].strip()
          
          JSON_Information.append(schema_copy)           
      else:
        if mode == "pub":
          if initial_row:
            initial_row = False
            i = 0
            # Maps the column titles to indices
            # which ensures that the script will
            # work even if the order changes
            for column in row:
              if column == "Team":
                team_index = i
                #print "team %i" % i
              if column == "Title":
                title_index = i
                #print "title %i" % i
              if column == "Link":
                link_index = i
                #print "link %i" % i
              i += 1
          else:
            #print row
            # Copies all relevant schema information
            # in a row to the JSON array.
            # Always uses a blank copy of the schema
            # to ensure that wrong information isn't 
            # copied.
            record = copy.deepcopy(schema)
            record['Title'] = row[title_index]
            record['Program Teams']=[row[team_index]]
            record['Link'] = row[link_index]
            JSON_Information.append(record)

        if mode == "project":
          if initial_row:
            initial_row = False
            i = 0
            # Maps the column titles to indices
            # which ensures that the script will
            # work even if the order changes
            for column in row:
              if column == "Team":
                team_index = i
              if column == "Project":
                project_index = i
              if column == "Category":
                category_index = i
              if column == "Code":
                code_index = i
              if column == "Public Homepage":
                home_index = i
              if column == "Description":
                description_index = i
              if column == "License":
                license_index = i
              i += 1
          else:
            # Copies all relevant schema information
            # in a row to the JSON array.
            # Always uses a blank copy of the schema
            # to ensure that wrong information isn't 
            # copied.
            record = copy.deepcopy(schema)
            record['Software'] = row[project_index]
            record['Program Teams']=[row[team_index]]
            record['External Link'] = row[home_index]
            record['Public Code Repo'] = row[code_index]
            record['Description'] = row[description_index]
            record['License'] = [row[license_index]]
 
            # Assumes the catagories of a project are seperated
            # by slashes e.g. Cloud/Cybersecurity/Big Data.
            # Will also trim non-important white space.
            categories = row[category_index].split('/')
            for j in xrange(len(categories)):
              category = categories[j]
              categories[j] = category.strip()
            record['Categories'] = categories

            JSON_Information.append(record)

  return JSON_Information

