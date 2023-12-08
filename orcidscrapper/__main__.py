import requests
import orcid
import toml
import argparse

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = toml.load(config_file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found.")
        return None

def controller(tomlpath, researcher_name):

    if tomlpath:
        config = load_config(tomlpath)

        if config:
            # Use the values from the config
            Client_ID = config.get('Client_ID', '')
            Client_secret = config.get('Client_secret', '')

    else:
        print("Error: Please provide a path to the TOML configuration file using --tomlpath.")

    api = orcid.PublicAPI(Client_ID, Client_secret)
    search_token = api.get_search_token_from_orcid()
    search_results = api.search(researcher_name, access_token=search_token)
    return search_results

def main():
    scriptname = 'orcID Scrapper' 
    parser = argparse.ArgumentParser()

    # Main Arguments
    parser.add_argument('--tomlpath', type=str, help='Path to the TOML configuration file')
    args = parser.parse_args()

    researcher_name = input("Enter researcher's name: ")
    affiliation = input("Enter affiliation: ")

    orcid_number = controller(args.tomlpath, researcher_name)

    if orcid_number:
        print(f"ORCID for {researcher_name} with affiliation {affiliation}: {orcid_number}")
    else:
        print(f"ORCID not found for {researcher_name} with affiliation {affiliation}")

if __name__ == "__main__":
    main()



    