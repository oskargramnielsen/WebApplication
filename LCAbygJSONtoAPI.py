
def JSONtoAPI():
    import requests
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
    import base64
    import time
    import random

    #plotting
    from matplotlib import pyplot
    import seaborn as sns

    warnings.filterwarnings("ignore")



    path = "C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\JSON_files\\"

    json_merged=[]

    #loading example file from LCAbyg and mergning them into one json-list.
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            
            f = open(file)
            f_load = json.load(f)
            json_merged = json_merged+f_load
            
    out_file = open("C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\LCAbyg_API\\api_in\\example_project.json", "w")
    
    json.dump(json_merged, out_file, indent = 2)
    
    out_file.close()

    with open("C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\RevitQuantities\\Building.txt") as f:
        contents = f.read()

    gfa = float(contents.split(",")[1])


    ###########################################################


    def send_job(input_path, output_path, username, password):
        print('Preparing data:')
        with open(input_path, 'r', encoding='utf-8') as f:
            input_json = f.read()
        target = 'lcabyg5_calc'
        user_group = 'Test'
        job_data = {
            'priority': 0,
            'job_target': target,
            'job_target_min_ver': '',
            'job_target_max_ver': '',
            'job_arguments': '',
            'input_blob': base64.standard_b64encode(input_json.encode('utf-8')).decode('utf-8'),
        }
        print()

        print('Finding a server:')
        job_queue_url = get_a_job_server(target, user_group)
        print(f'job_queue_url = {job_queue_url}')
        print()

        print('Sending ping:')
        res_ping = ping(job_queue_url)
        print(f'res_ping = {res_ping}')
        print()

        print('Logging in:')
        token = login(job_queue_url, username, password)
        print(f'token = {token}')
        print()

        print('Submitting a new job:')
        job_id = new_job(job_queue_url, token, job_data)
        print(f'job_id = {job_id}')
        print()

        print('Waiting for the job to finish:')
        done = False
        while not done:
            status = job_status(job_queue_url, token, job_id)
            print(f'status = {status["status"]}')
            done = (status['status'] == 'Ready') or (status['status'] == 'Failed')
            time.sleep(1)
        print()

        print('Download the results:')
        job_output_raw = get_job_output(job_queue_url, token, job_id)
        job_output = base64.b64decode(job_output_raw).decode('utf-8')
        print()

        print('Saving the results to disk:')
        data = json.loads(job_output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print()

        print('Done')

    DIRECTORY_URL = 'https://swa-dir-a.buildsrv.dk'


    def get_a_job_server(target, user_type):
        res = requests.get(DIRECTORY_URL).json()

        assert res['version'] == 1

        alternatives = list()
        for srv in res['job_queues']:
            if target in srv['supported_targets'] and user_type in srv['allowed_users']:
                alternatives.append(srv)

        assert len(alternatives) > 0
        return random.choice(alternatives)['url']


    def ping(job_queue_url):
        res = requests.get(f'{job_queue_url}/v1/ping').text
        assert res == 'pong'
        return res


    def login(job_queue_url, username, password):
        data = {
            'username': username,
            'password': password,
        }
        json_data = json.dumps(data)
        res = requests.post(f'{job_queue_url}/v1/login', json_data)
        data = json.loads(res.text)
        return data


    def new_job(job_queue_url, token, job_data):
        auth_headers = {
            'Session': token,
        }
        res = requests.post(f'{job_queue_url}/v1/jobs', json=job_data, headers=auth_headers)
        data = json.loads(res.text)
        return data


    def job_status(job_queue_url, token, job_id):
        auth_headers = {
            'Session': token,
        }
        res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}', headers=auth_headers)
        return res.json()


    def job_delete(job_queue_url, token, job_id):
        auth_headers = {
            'Session': token,
        }
        res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}', headers=auth_headers)
        return res.json()


    def get_job_output(job_queue_url, token, job_id):
        auth_headers = {
            'Session': token,
        }
        res = requests.get(f'{job_queue_url}/v1/jobs/{job_id}/output', headers=auth_headers)
        return res.json()


    def send_job(input_path, output_path, username, password):
        print('Preparing data:')
        with open(input_path, 'r', encoding='utf-8') as f:
            input_json = f.read()
        target = 'lcabyg5_calc'
        user_group = 'Test'
        job_data = {
            'priority': 0,
            'job_target': target,
            'job_target_min_ver': '',
            'job_target_max_ver': '',
            'job_arguments': '',
            'input_blob': base64.standard_b64encode(input_json.encode('utf-8')).decode('utf-8'),
        }
        print()

        print('Finding a server:')
        job_queue_url = get_a_job_server(target, user_group)
        print(f'job_queue_url = {job_queue_url}')
        print()

        print('Sending ping:')
        res_ping = ping(job_queue_url)
        print(f'res_ping = {res_ping}')
        print()

        print('Logging in:')
        token = login(job_queue_url, username, password)
        print(f'token = {token}')
        print()

        print('Submitting a new job:')
        job_id = new_job(job_queue_url, token, job_data)
        print(f'job_id = {job_id}')
        print()

        print('Waiting for the job to finish:')
        done = False
        while not done:
            status = job_status(job_queue_url, token, job_id)
            print(f'status = {status["status"]}')
            done = (status['status'] == 'Ready') or (status['status'] == 'Failed')
            time.sleep(1)
        print()

        print('Download the results:')
        job_output_raw = get_job_output(job_queue_url, token, job_id)
        job_output = base64.b64decode(job_output_raw).decode('utf-8')
        print()

        print('Saving the results to disk:')
        data = json.loads(job_output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print()

        print('Done')


    def main():
        username = "oskargram1996@gmail.com"
        password = "da3f75d0-a94f-4700-ba7c-39882cb0f0bc"

        input_json = "C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\LCAbyg_API\\api_in\\example_project.json"
        output_json = "C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\LCAbyg_API\\api_out\\result_json.json"

        

        send_job(input_json, output_json, username, password)

    main()

    with open("C:\\Users\\oskar\\OneDrive - Danmarks Tekniske Universitet\\Kandidat Speciale\\Programmering\\RevitQuantities\\Building.txt") as f:
        contents = f.read()

    gfa = float(contents.split(",")[1])
    
    file = r"C:\Users\oskar\OneDrive - Danmarks Tekniske Universitet\Kandidat Speciale\Programmering\LCAbyg_API\api_out\result_json.json"

    f = open(file)
    f_load = json.load(f)

    building_id = '6d766aa5-50aa-4005-ab35-29f2fb82ddad'

    results = f_load['results'][building_id]['SumNew']['9999']

    df = pd.DataFrame((results).items(), columns=['Impact Categories', 'Value total'])

    a4_dims = (15, 5)

    fig, ax = pyplot.subplots(figsize=a4_dims)

    sns.barplot(ax = ax, data=df, x="Impact Categories", y="Value total")

    df['Value / m2 / year'] = round(df['Value total']/(gfa*50),2)

    a4_dims = (15, 5)

    fig, ax = pyplot.subplots(figsize=a4_dims)

    sns.barplot(ax = ax, data=df, x="Impact Categories", y="Value / m2 / year")

    import codecs
    f=codecs.open("RunLCA.html", 'r')

    return f