open-catalog-generator
======================

Code and templates required to build the DARPA open catalog.

basic structure
=========================

- The Open Catalog website is generated by Python scripts which draw information from JSON files.

- The Python scripts that generate the site are located under the scripts folder, the most important being **generate_html.py**.

- All of the information about the projects are from JSON files that are located in the **darpa\_open\_catalog** folder (which is a separate repository on Github).

- There are three main types of JSON files, **pubs**, **program**, and **software**. The basic naming structure is to have the name of the DARPA Program such as XDATA and then a dash followed by one of the three keywords mentioned above. An example of this is **XDATA-software.json**.

- **pubs** JSON files contain information about the references (APA/MLA/etc) program teams have used for their projects.

- **software** JSON files contain information about any software that has been developed in the program/that will be listed in the catalog.

- **program** JSON files contain information about the DARPA Program itself.

- There are two special JSON files, **active\_content.json** and **active\_content\_deployed.json**. Both files list all the active programs inside of the open catalog, but the difference, is that the deployed file only lists programs that will appear on the DARPA website. Basically, the **active\_content\_deployed.json** file is a subset of the **active\_content**.json file.

open catalog updates
=========================

- New and updated data is typically sent and entered in by the performers, although it must be checked to ensure that it follows a proper format.

- Data is sent in many forms such as Excel Spreadsheets, word documents, and JSON files that don’t follow the catalog’s schemas. Performer data must be transformed to fit the schemas used by the three different types of JSON files.

- There are scripts located in the **transforms** folder to help transform the data into a properly formatted JSON file, the most important is **transform\_into\_JSON.py**. There is a readme inside of the folder that includes instructions for use.

- There are scripts located in the **scripts** folder and **test** folder that can help test/check the data. For instance, there is a script called **test_urls.py** inside the **test** folder which checks if the URLs included in the JSON files work.

makefile/build process
=========================

- The catalog uses a **Makefile** to easily run scripts and build the website. Most important functions of the open catalog generator can be called with a single make command.

- Running the command “**Make datainit**” will bring a current version of all open catalog JSON files into the directory, this command must be used to ensure that all information is current.

- Running the command “**Make**” will generate a version of the website which includes normal hyperlinks and all active content.

- Running the command “**Make deploy**” will generate a version of the website that will be deployed on DARPA’s website.

add_json_fields.py
=========================
Steps for adding json fields to a specific file type:

1. Open the json file for the program that needs to be added or modified. Add a blank("") entry to the program json for both the "Display Software Columns" and "Display Pubs Columns" fields. See the following example:

    "Display Software Columns":[
        "Team",
        "Project",
		"",
        "Category",
        "Code",
        "Description",
        "License"
    ],
    "Display Pubs Columns":[
        "Team",
        "Title",
		"",
        "Link"
    ],

2. From the scripts directory, open the add_json_fields.py script in an editor. 

3. There are three parameters that need to be passed into the make script:
  3a. file_types: This parameter should contain only the type(s) of files that you wish to add fields to. Valid values are "office", "program", "software" and "pubs"
  3b. new_fields: This parameter is a key-value pair object that takes the field name as the key and the field value as the value. There is no limit to the number of key-value pairs that can be added.
  3c. insert_after: The added field(s) will be placed after the given field name. The given field name can also be left empty "", which by default appends the added fields to the end of the json object 
  
4. The Makefile contains an executable definition that can be used to quickly run this script. Using the CYGWIN command line, run the following command with NO SPACES between commas:

	make addfields FILE_TYPES="file_type1" NEW_FIELDS="field1:value1,field2:value2" INSERT_AFTER="field_name"
	e.g. make addfields FILE_TYPES="pubs,software" NEW_FIELDS="Test 1:pass,Test 2:fail,Test Options:[pass,fail]" INSERT_AFTER="Program Teams"

5. Verify that the fields were added correctly and to the appropriate files by reviewing the new files in the "darpa_open_catalog/new_json" directory. If the files are correct, move them to the "darpa_open_catalog" directory and done! Now there are new json files for the next build!

6. Be sure to delete the "new_json" directory from the "darpa_open_catalog" directory so that it is not mistakenly committed to the project repository. 

Note: The json files that are reproduced are based on the active_content.json file. Be sure to add all of the json files that are to be reproduced to the active_content.json file before running the addjsonfields script.


convert_non_ascii_chars.py
=========================
Steps for converting/removing non-ascii characters from json files:

1. In the "darpa_open_catalog" directory, record the name of the file(s) that include non-ascii characters in order to use them as parameters in the script. 
 
2. The Makefile contains an executable definition that can be used to quickly run this script after modifying the variable. Using the CYGWIN command line, run the following command with NO SPACES between the filenames:
   
   make fileascii FILES="filename1,filename2,filename3"
   e.g. make fileascii FILES="CRASH-program.json,CRASH-pubs.json"

3. Verify that the non-ascii characters were replaced/removed by opening the new files in the "darpa_open_catalog/new_json" directory. If the files are correct, move them to the "darpa_open_catalog" directory and done! Now there are new json files for the next build!

4. Be sure to delete the "new_json" directory from the "darpa_open_catalog" directory so that it is not mistakenly committed to the project repository. 

Note: In some cases, a non-ascii character may not be mapped to an ascii character, therefore causing the character to be replaced with another non-ascii character or removed completely. If the character needs an ascii equivalent, an exception will need to be added to the "hex2ascii" method in the script to identify an ascii character to replace the character.

  def hex2ascii(hex):
    uni_num = int(hex,16)
    #print "uni_num: %s \r" % uni_num 
    if uni_num > 127:
      if uni_num == 8243:
        char_out = '"'
		.
		.
		.
