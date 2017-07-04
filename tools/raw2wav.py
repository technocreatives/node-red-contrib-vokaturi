#!/usr/bin/env python
import sys,os
import json
import sox


#initialize data to be output
data = {}
data['valid'] = 0 ;

if ( len(sys.argv) != 2 ) :
    print("No war file provided")
    print("Usage "+ sys.argv[0] +" <path/to/raw>")
    data['error'] = "No .raw file provided";
    print(json.dumps(data));
    exit(-1);

file_name = sys.argv[1];
if os.path.isfile(file_name):

    try:
        tfm = sox.Transformer();
        converted_file_name = file_name + ".wav";
        tfm.set_input_format(file_type="raw",rate=16000,bits=16,encoding="signed-integer");
        tfm.build(file_name,converted_file_name);
        data['filename'] = converted_file_name;
        data['valid'] = 1;
    except:
        data['error'] = "unable to convert raw file. Check sox paramaters"
else:
    data['error'] = "The provided filename doesn't exist"

json_data = json.dumps(data);

print(json_data)
