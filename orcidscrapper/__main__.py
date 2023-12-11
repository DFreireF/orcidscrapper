import requests
import orcid
import toml
import argparse
import ezodf

def read_ods(odsin):
    try:
        with open(odsin, 'r') as f:
            pass
    except FileNotFoundError:
        print(f'File not found: {odsin}')
    except PermissionError:
        print(f'Permission denied: cannot read {odsin}')
    except Exception as e:
        print('Error reading file:', e)
        
    # Open the .ods file    
    odsinfo = ezodf.opendoc(odsin)
    # Get the first sheet
    sheet = odsinfo.sheets[0]
    author_first_names, author_last_names, affiliations = [[] for i in range(3)]
    for row in range(1, sheet.nrows()): #We skip the first row with the 'Titles'
        # Loop through the columns in the row
        for col in range(0, sheet.ncols()):
            # Get the cell value
            cell = sheet[row, col].value
    
            if col == 0: first_name = cell
            elif col == 2: last_name = cell
            elif col == 3: continue #emails
            elif col == 4: continue #ORCID
            elif col == 5: affiliation = cell # We only take the first affiliation

        if (first_name or last_name) is None: 
            print('names missing')
            break

        author_first_names.append(first_name)
        author_last_names.append(last_name)
        affiliations.append(affiliation)

    return author_first_names, author_last_names, affiliations

def write_ods(odsout, orcid_id, orcid_uri, row_index):
    doc = ezodf.opendoc(odsout)
    sheet = doc.sheets[0]
    sheet[row_index, 4].set_value(orcid_id)
    sheet[row_index, 8].set_value(orcid_uri)
    doc.save()

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = toml.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return None

def controller(tomlpath, first_name, last_name, affiliation = None):

    if tomlpath:
        config = load_config(tomlpath)

        if config:
            # Use the values from the config
            Client_ID = config.get('Client_ID', '')
            Client_secret = config.get('Client_secret', '')

    else:
        print('Error: Please provide a path to the TOML configuration file using --tomlpath.')

    api = orcid.PublicAPI(Client_ID, Client_secret)
    search_token = api.get_search_token_from_orcid()
    query = 'given-names="{0}"family-names="{1}"{2}'.format(first_name, last_name, f'institution-name="{affiliation}"' if affiliation else '')
    search_results = api.search(query, access_token=search_token)
    return search_results

def main():
    scriptname = 'orcID Scrapper' 
    parser = argparse.ArgumentParser()

    # Main Arguments
    parser.add_argument('--tomlpath', type=str, help='Path to the TOML configuration file')
    parser.add_argument('--ods', type=str, help='Path to the ods spreedsheet with the author list')
    args = parser.parse_args()

    if args.ods:
        author_first_names, author_last_names, affiliations = read_ods(args.ods)
        for i, (first_name, last_name, affiliation) in enumerate(zip(author_first_names, author_last_names, affiliations)):
            try:
                print(i, first_name, last_name, affiliation)
                orcid_results = controller(args.tomlpath, first_name, last_name, affiliation = affiliation)['result'][0]['orcid-identifier']
                orcid_id = orcid_results['path']
                orcid_uri = orcid_results['uri']
                print(orcid_uri)
                row_index = i + 1
                write_ods(args.ods, orcid_id, orcid_uri, row_index)
            except:
                print('except') 
                continue

    else:
        first_name = input("Enter researcher's first name: ")
        last_name = input("Enter researcher's last name: ")
        affiliation = input('Enter affiliation: ')

        orcid_results = controller(args.tomlpath, first_name, last_name, affiliation = affiliation)

        if orcid_results and 'result' in orcid_results:
            first_result = orcid_results['result'][0]
            orcid_identifier = first_result['orcid-identifier']['uri']
            orcid_number = first_result['orcid-identifier']['path']
            print(f'ORCID for {first_name} {last_name} with affiliation {affiliation}: {orcid_number} and uri {orcid_identifier}')
        else:
            print(f'ORCID not found for {first_name} {last_name} with affiliation {affiliation}')

    

if __name__ == '__main__':
    main()



    