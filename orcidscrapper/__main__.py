import requests

def get_orcid_number(researcher_name, affiliation):
    search_url = f"https://orcid.org/orcid-search/search?queryText={researcher_name}+affiliation:{affiliation}&rows=1"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        if "result" in data and data["result"]:
            return data["result"][0]["orcid-identifier"]["path"]
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response content: {response.content.decode('utf-8')}")
        return None

def main():
    researcher_name = input("Enter researcher's name: ")
    affiliation = input("Enter affiliation: ")

    orcid_number = get_orcid_number(researcher_name, affiliation)

    if orcid_number:
        print(f"ORCID for {researcher_name} with affiliation {affiliation}: {orcid_number}")
    else:
        print(f"ORCID not found for {researcher_name} with affiliation {affiliation}")

if __name__ == "__main__":
    main()
