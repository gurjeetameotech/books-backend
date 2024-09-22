from flask import Flask, request, jsonify
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# Function to add authors to the Author table in Notion

def add_authors_to_notion(author_table_id, author_names):
    notion_api_url = "https://api.notion.com/v1/pages"
    search_url = f"https://api.notion.com/v1/databases/ffff0618cfa58172a5f4c9cefd04f3a5/query"

    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    author_ids = []

    # Function to check if an author already exists
    def author_exists(author_name):
        search_payload = {
            "filter": {
                "property": "Name",
                "title": {
                    "contains": author_name
                }
            }
        }
        response = requests.post(search_url, headers=headers, json=search_payload)

        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                # If the author exists, return the ID
                return results[0]['id']
            else:
                return None
        else:
            print(f"Error checking for existing author: {response.text}")
            return None

    for author_name in author_names:
        # Check if the author already exists
        existing_author_id = author_exists(author_name)

        if existing_author_id:
            print(f"Author '{author_name}' already exists. Using existing ID.")
            author_ids.append(existing_author_id)
            continue

        # If the author doesn't exist, add them
        data = {
            "parent": {
                "database_id": "ffff0618cfa58172a5f4c9cefd04f3a5"  # Use the correct author table ID
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": author_name
                            }
                        }
                    ]
                }
            }
        }

        response = requests.post(notion_api_url, headers=headers, json=data)

        if response.status_code == 200:
            author_data = response.json()
            author_ids.append(author_data['id'])  # Save the author ID
        else:
            return {"error": response.text, "status_code": response.status_code}

    return author_ids


# Function to add genres to the Genre table in Notion
def add_genres_to_notion(genre_table_id, genre_names):
    notion_api_url = "https://api.notion.com/v1/pages"
    search_url = f"https://api.notion.com/v1/databases/ffff0618cfa5814f822bc8e9c866c4d6/query"

    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    genre_ids = []

    # Function to check if a genre already exists
    def genre_exists(genre_name):
        search_payload = {
            "filter": {
                "property": "Name",
                "title": {
                    "equals": genre_name
                }
            }
        }
        response = requests.post(search_url, headers=headers, json=search_payload)

        if response.status_code == 200:
            results = response.json()["results"]
            if results:
                # If the genre exists, return the ID
                return results[0]['id']
            else:
                return None
        else:
            print(f"Error checking for existing genre: {response.text}")
            return None

    for genre_name in genre_names:
        # Check if the genre already exists
        existing_genre_id = genre_exists(genre_name)

        if existing_genre_id:
            print(f"Genre '{genre_name}' already exists. Using existing ID.")
            genre_ids.append(existing_genre_id)
            continue

        # If the genre doesn't exist, create a new one
        data = {
            "parent": {
                "database_id": "ffff0618cfa5814f822bc8e9c866c4d6"  # Use the correct genre table ID
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": genre_name
                            }
                        }
                    ]
                }
            }
        }

        response = requests.post(notion_api_url, headers=headers, json=data)

        if response.status_code == 200:
            genre_data = response.json()
            genre_ids.append(genre_data['id'])  # Save the genre ID
        else:
            return {"error": response.text, "status_code": response.status_code}

    return genre_ids


# Function to add a book to the Book table in Notion
def post_to_notion(database_id, title, price,publisher, image,author_ids, page_count, language, status, genre_ids):
    print(publisher, '3333333333333333333333333333333333333')
    print(image, '4444444444444444444444444444444444444444')
    notion_api_url = "https://api.notion.com/v1/pages"
    search_url = f"https://api.notion.com/v1/databases/ffff0618cfa5815e8043d9a775d32835/query"

    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    # Function to check if a book with the same title already exists
    def book_exists(title):
        search_payload = {
            "filter": {
                "property": "Book Name",
                "title": {
                    "equals": title
                }
            }
        }
        response = requests.post(search_url, headers=headers, json=search_payload)

        if response.status_code == 200:
            results = response.json()["results"]
            return len(results) > 0  # Return True if book exists, otherwise False
        else:
            print(f"Error checking for existing book: {response.text}")
            return False

    # Check if the book already exists
    if book_exists(title):
        return {"error": f"Book with title '{title}' already exists."}

    # If the book doesn't exist, create a new one
    data = {
        "parent": {
            "database_id": "ffff0618cfa5815e8043d9a775d32835"
        },
        "properties": {
            "Book Name": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Price": {
                "number": price
            },
            "Publisher": {
                "rich_text": [
                    {
                        "text": {
                            "content": publisher
                        }
                    }
                ]
            },
            "Book cover": {
                "files": [
                    {
                        "name": "Book Cover Image",
                        "external": {
                            "url": "http://books.google.com/books/content?id=8cxlDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api" + "&filetype=jpg"
                        }
                    }
                ]
            },
            "Author": {
                "relation": [{"id": author_id} for author_id in author_ids]
            },
            "Genre": {
                "relation": [{"id": genre_id} for genre_id in genre_ids]
            },
            "Total pages": {
                "number": page_count
            },
            "Language": {
                "select": {
                    "name": language
                }
            },
            "Status": {
                "status": {
                    "name": status
                }
            }
        }
    }

    response = requests.post(notion_api_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text, "status_code": response.status_code}


@app.route('/add-book', methods=['GET'])
def add_book():
    # Get query parameters from URL
    author_table_id = request.args.get('author_table_id')
    genre_table_id = request.args.get('genre_table_id')  # New genre table ID
    database_id = request.args.get('database_id')
    title = request.args.get('title')
    image = request.args.get('previewLink')

    image = str(image + "&filetype=jpg")
    price = request.args.get('price', type=float)
    price = int(price)
    publisher = request.args.get('publisher')
    print(publisher, "00000000000000000000000000000000")
    print(image, "111111111111111111111111111111111111")
    authors = request.args.getlist('authors')  # Author names
    genres = request.args.getlist('genre')  # Genre names to be added to the Genre table
    page_count = request.args.get('page_count', type=int)
    language = request.args.get('language')
    if language == 'en':
        language = "English"
    status = request.args.get('status')
    if status == 'Library':
        status = "Not started"

    author_ids = add_authors_to_notion(author_table_id, authors)

    if "error" in author_ids:
        return jsonify(author_ids)

    genre_ids = add_genres_to_notion(genre_table_id, genres)

    if "error" in genre_ids:
        return jsonify(genre_ids)

    response = post_to_notion(
        database_id, title, price, publisher,image, author_ids,page_count, language, status,  genre_ids)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
