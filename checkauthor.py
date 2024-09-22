import requests
import os


def query_notion_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": f"Bearer {os.getenv('NOTION_API_KEY')}",
        "Content-Type": "application/json"
    }

    # Define the filter and sort options
    data = {
        "filter": {
            "or": [
                {
                    "property": "Favourite",
                    "checkbox": {
                        "equals": True
                    }
                },
                {
                    "property": "Books count",
                    "number": {
                        "greater_than_or_equal_to": 2
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "Date of birth",
                "direction": "ascending"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"


# Usage
database_id = 'ffff0618-cfa5-8172-a5f4-c9cefd04f3a5'
database_response = query_notion_database(database_id)

if isinstance(database_response, dict):
    # Extracting the Author names from the response
    authors = [
        result['properties']['Name']['title'][0]['plain_text']
        for result in database_response.get('results', [])
        if result['properties']['Name']['title']  # Ensure there's a title property
    ]
    print(authors)
else:
    print(database_response)
