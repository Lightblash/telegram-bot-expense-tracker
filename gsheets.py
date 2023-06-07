import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_spreadsheet(client_secret: str, title: str) -> gspread.Spreadsheet:
    """
    Get Google Spreadsheet object by title

    Google Spreadsheet must be shared with client_email which
    is included in client_secret.json before using this function

    Parameters
    ----------
    client_secret : str
        Path to the client_secret.json file. This file can be obtained
        from the Google Developers Console in your project.

    title : str
        Title of the spreadsheet

    Returns
    -------
    Spreadsheet object
    """
    # Define scopes for our Google Console Developers App
    SCOPES = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        # Load service account info from the client_secret.json file
        service_account_info = json.loads(client_secret)

        # Initialize service account credentials
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            service_account_info, scopes=SCOPES
        )

        # Authorize and create the Google Sheets API client
        gs_client = gspread.authorize(creds)

        # Get the spreadsheet object by title
        spreadsheet = gs_client.open(title)

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File {client_secret} not found") from exc
    except gspread.exceptions.SpreadsheetNotFound as exc:
        raise Exception("Spreadsheet not found!") from exc

    return spreadsheet
