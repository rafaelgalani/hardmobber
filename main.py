debug = False
quiet_update = False

# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from time import strftime

import requests as r, json, time, webbrowser, os

# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

results_file_name = 'hardmob-results.json'
script_dir = os.path.dirname(__file__)
result_file_path = os.path.join(script_dir, results_file_name)

toaster = ToastNotifier()
results = list()
update_seconds_interval = 5

# --------------------------------------------------------------------------------------------------------------------------------------------------------- #

if debug:
    print('Initializing.')
    print('Interval => {} seconds.'.format(update_seconds_interval))

def scrape():
    soup = perform_get_request('https://www.hardmob.com.br/forums/407-Promocoes?s=&pp=30&daysprune=-1&sort=dateline&order=desc')

    previous_results = get_previous_values()
    threads = soup.select('h3.threadtitle > a.title')

    for thread in threads:
        thread_id = thread['id'].split('_')[2]

        if debug:
            print('Thread id: {}'.format(thread_id))
            print('Is thread retrieved? {}'.format(thread_id in previous_results))

        if thread_id not in previous_results:
            previous_results.append(thread_id)

            results.append({
                "text": thread.text,
                "id": thread_id
            })

    has_new_results = len(results)
    
    if has_new_results:
        if not quiet_update:
            if debug:
                print('Showing new results... Updating {} seconds after showing all results.'.format(update_seconds_interval), end='\n')
            else:
                pass
                
            for result in results:
                print('{} => {}'.format(strftime('%H:%M'), result['text']))
                toaster.show_toast('Clique para abrir', result['text'], duration=2, callback_on_click=lambda: open_url(result['id']))
        else:
            if debug:
                print('Dumping retrieved threads to the JSON result file...')
        
    else:
        if debug: 
            print('No new results. Updating after {} seconds...'.format(update_seconds_interval))
        else:
            pass
    
    if has_new_results:
        with open(result_file_path, 'w') as json_file:
            json.dump(previous_results, json_file)

    if quiet_update:
        if debug:
            print('Results dumped. Exiting script in {} seconds...'.format(update_seconds_interval))
        time.sleep(update_seconds_interval)
        exit()

    results.clear()

def open_url(thread):
    webbrowser.open_new_tab('https://www.hardmob.com.br/threads/{}'.format(thread))

def perform_get_request(url):
    s = r.Session()
    res = s.get(url)
    
    if debug:
        print('Status code => {}'.format(res.status_code))

    return BeautifulSoup(res.content, 'html.parser')

def get_previous_values():
    prev_results = list()

    if debug:
        print("Directory: {}".format(script_dir))
        print("Final path: {}".format(result_file_path))

    try:
        with open(result_file_path, 'r') as json_file:
            if debug:
                print('Found results file. Loading previous results...')
            prev_results = json.loads(json_file.read())
    except FileNotFoundError:
        if debug:
            print("Results file not found. Creating file @ script's path...")

        with open(result_file_path, 'w') as json_file:
            json.dump(results, json_file)

        with open(result_file_path, 'r') as json_file:
            prev_results = json.loads(json_file.read())

    if debug:
        print('Previous results => {}'.format(prev_results))

    return prev_results

while True:
    scrape()
    if debug:
        print('Sleeping for {} seconds...'.format(update_seconds_interval))
    time.sleep(update_seconds_interval)
    if debug:
        print('Woke up. Retrieving again...')