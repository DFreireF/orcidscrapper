# ORCID Scraper

This script is designed to retrieve ORCID numbers from the ORCID Public API based on the names of researchers in a spreadsheet and update the spreadsheet with the obtained ORCID information.

## Prerequisites

- Python 3.x
- Required Python packages (install using `pip install package_name`):
  - `requests`
  - `orcid`
  - `ezodf`
  - `toml`

## Usage

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DFreireF/orcidscrapper.git
   cd orcidscrapper
   ```

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. Prepare your configuration file:

Create a TOML configuration file (config.toml) with your ORCID Public API credentials:

    ```toml
    Client_ID = "your_client_id"
    Client_secret = "your_client_secret"
    ```

Run the script:

    ```bash
    python __main__.py --tomlpath config.toml --ods your_spreadsheet.ods
    ```

If you want to interactively enter the researcher's information, simply run the script without the --ods argument:

    ```bash
    python __main__.py --tomlpath config.toml
    ```

Note: If the spreadsheet does not exist or is not found, the script will prompt you for researcher information interactively.