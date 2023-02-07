def CreateJSON():
    #imports

    import csv
    from flask import Flask, render_template, url_for
    import os
    import json
    import pandas as pd
    import uuid
    import sys
    import stat
    import json
    import warnings
    import openpyxl
    warnings.filterwarnings("ignore")

    # Loading JSON file function
    def load_json(file_name):

        # json_floor.json
        f = open('C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\RevitQuantities\\' + file_name)
        
        # returns JSON object as 
        # a dictionary

        data = json.load(f)

        # Iterating through the json
        df = pd.DataFrame({'Type':[],'ElementId':[],'LayerId':[],'MaterialId':[],'Name':[],'Area':[],'Thickness':[]})

        # creating dataframe from json format
        for i in data:
            df=df.append({'Type':i['Type'],
                            'ElementId':i['ElementId'],
                            'LayerId':i['LayerId'],
                            'MaterialId':i['MaterialId'],
                            'Name':i['Name'],
                            'Area':i['Area'],
                            'Thickness':i['Thickness']},
                            ignore_index=True)
        f.close()

        return df

    def export_json(file, filename):

        path = "C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\JSON_files"

        dir = os.path.join(path, filename)

        with open(dir + ".json", 'w', encoding = 'utf-8') as f:
            json.dump(file, f, indent=2, ensure_ascii = False)

        path = "C:\Program Files\SBi\LCAbyg 5 (64 bit) (5.2.1.0)\import_example"

        dir = os.path.join(path, filename)

        with open(dir + ".json", 'w', encoding = 'utf-8') as f:
            json.dump(file, f, indent=2, ensure_ascii = False)

            
    df_floor = load_json('json_floor.json')
    df_ceiling = load_json('json_ceiling.json')
    df_roof = load_json('json_roof.json')
    df_wall = load_json('json_wall.json')
    
    frames = [df_floor, df_ceiling, df_roof, df_wall]
    df = pd.concat(frames,ignore_index =True)

    # con_list = list(pd.read_csv(r"C:\Users\oskar\OneDrive - Danmarks Tekniske Universitet\Kandidat Speciale\Programmering\const.csv"), delimiter=',')
    con_list = pd.read_excel(r"C:\Users\oskar\OneDrive - Danmarks Tekniske Universitet\Dokumenter\const1.xlsx") # can also index sheet by name or fetch all sheets
    con_list = con_list['id'].tolist()

    node_list = []
    edge_list = []
    cat_list = []
    print(con_list)
    for i in range(len(df)):
        # print(df['MaterialId'][i])

        if df['MaterialId'][i] == None:
            # print(df['MaterialId'][i])    

            MaterialId = "72e6c484-77a8-5b22-b14e-e02b4b1339e4"

        elif df['MaterialId'][i] in con_list:
            print(df['MaterialId'][i])
            print("works")
            MaterialId = df['MaterialId'][i]

        else:
            # print("work")

            MaterialId = "72e6c484-77a8-5b22-b14e-e02b4b1339e4"


        element_edgeId = str(uuid.uuid4())
        element_cat_edgeId = str(uuid.uuid4())

        if df['Type'][i] == "Walls":
            element_name = 'Wall ' + df['ElementId'][i] 
            element_type = '10a52123-48d7-466a-9622-d463511a6df0'

        elif df['Type'][i] == "Roofs":
            element_name = 'Roof ' + df['ElementId'][i] 
            element_type = 'd734712a-d27d-42c5-936f-98fe4c4df90b'

        elif df['Type'][i] == "Ceilings":
            element_name = 'Ceiling ' + df['ElementId'][i] 
            element_type = 'f4c234ec-77f1-4ee0-92d0-f1819e0307d4'

        elif df['Type'][i] == "Floors":
            element_name = 'Floor ' + df['ElementId'][i] 
            element_type = '2ffe16fd-f0c9-4d31-a31a-f96d58d3df95'

        if int(df['LayerId'][i]) == 1:
            
            element_nodeId = str(uuid.uuid4())
            
            element_node = {
                "Node": {
                    "Element": {
                        "id": element_nodeId,
                        "name": {
                            "Danish": element_name,
                            "English": "",
                            "German": ""
                        },
                        "source": "User",
                        "comment": "",
                        "enabled": True,
                        "active": True
                    }
                }
            }
            element_edgenode = {
                "Edge": [
                    {
                        "ElementToConstruction": {
                            "id": element_edgeId,
                            "amount": df['Area'][i],
                            "enabled": True
                        }
                    },
                    element_nodeId,
                    MaterialId
                ]
            }
            element_cat_edge = {
                "Edge": [
                    {
                        "CategoryToElement": {
                            "id": element_cat_edgeId,
                            "enabled": True
                        }
                    },
                    element_type,
                    element_nodeId
                ]
            }

            node_list.append(element_node)
            edge_list.append(element_edgenode)
            cat_list.append(element_cat_edge)
            
        else:
            element_edge = {
                    "Edge": [
                        {
                            "ElementToConstruction": {
                                "id": element_edgeId,
                                "amount": df['Area'][i],
                                "enabled": True
                            }
                        },
                        element_nodeId,
                        MaterialId
                    ]
                }

            edge_list.append(element_edge)


    elements = node_list + edge_list


    export_json(elements,"elements")
    export_json(cat_list,"element_category_edges")

    # df.to_dict('index')
    import codecs
    f=codecs.open("DataUpdated.html", 'r')

    return f