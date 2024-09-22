from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Function to add authors to the Author table in Notion
def add_authors_to_notion(author_table_id, author_names):
    notion_api_url = "https://api.notion.com/v1/pages"
    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    author_ids = []

    for author_name in author_names:
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
    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    genre_ids = []

    for genre_name in genre_names:
        data = {
            "parent": {
                "database_id": "ffff0618cfa5813a9360f5ceea1eec9a"  # Use the correct genre table ID
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
def post_to_notion(database_id, title, price, publisher, author_ids, page_count, language, status, due_date, tags, genre_ids):
    notion_api_url = "https://api.notion.com/v1/pages"
    headers = {
        "Notion-Version": "2022-02-22",
        "Authorization": "Bearer secret_DJxHTL2hTPs8qHW0MgVlgrh2rrdvfJMkEKI7ogPySF4",
        "Content-Type": "application/json"
    }

    data = {
        "parent": {
            "database_id": database_id
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
            "Author": {
                "relation": [{"id": author_id} for author_id in author_ids]
            },
            "genres": {
                "relation": [{"id": genre_id} for genre_id in genre_ids]
            },
            "Page Count": {
                "number": page_count
            },
            "Language": {
                "select": {
                    "name": language
                }
            },
            "Status": {
                "select": {
                    "name": status
                }
            },
            "Due Date": {
                "date": {
                    "start": due_date
                }
            },
            "Tags": {
                "multi_select": [{"name": tag.strip()} for tag in tags]
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
    price = request.args.get('price', type=float)
    publisher = request.args.get('publisher')
    authors = request.args.getlist('authors')  # Author names
    genres = request.args.getlist('genre')  # Genre names to be added to the Genre table
    page_count = request.args.get('page_count', type=int)
    language = request.args.get('language')
    status = request.args.get('status')
    due_date = request.args.get('due_date')
    tags = request.args.get('tags', '').split(',')

    # Step 1: Add authors to the Author table and get their IDs
    author_ids = add_authors_to_notion(author_table_id, authors)

    if "error" in author_ids:
        return jsonify(author_ids)  # Return error if adding authors failed

    # Step 2: Add genres to the Genre table and get their IDs
    genre_ids = add_genres_to_notion(genre_table_id, genres)

    if "error" in genre_ids:
        return jsonify(genre_ids)  # Return error if adding genres failed

    # Step 3: Add the book to the Book table using author and genre IDs
    response = post_to_notion(
        database_id, title, price, publisher, author_ids, page_count, language, status, due_date, tags, genre_ids)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)




# @app.route('/add-book', methods=['GET'])
# def add_book():
#     # Get query parameters from URL
#     author_table_id = request.args.get('author_table_id')
#     genre_table_id = request.args.get('genre_table_id')  # New genre table ID
#     database_id = request.args.get('database_id')
#     title = request.args.get('title')
#     image = request.args.get('previewLink')
#     price = request.args.get('price', type=float)
#     publisher = request.args.get('publisher')
#
#     # publishedDate = request.args.get('publishedDate')
#     # print(publishedDate, '=====================================')
#     authors = request.args.getlist('authors')  # Author names
#     genres = request.args.getlist('genre')  # Genre names to be added to the Genre table
#     page_count = request.args.get('page_count', type=int)
#     language = request.args.get('language')
#     if language == 'en':
#         language = "English"
#     status = request.args.get('status')
#     if status == 'Library':
#         status = "Not started"
#
#     author_ids = add_authors_to_notion(author_table_id, authors)
#
#     if "error" in author_ids:
#         return jsonify(author_ids)
#
#     genre_ids = add_genres_to_notion(genre_table_id, genres)
#
#     if "error" in genre_ids:
#         return jsonify(genre_ids)
#
#     response = post_to_notion(
#         database_id, title, price, publisher,author_ids,image, page_count, language, status,  genre_ids)
#
#     return jsonify(response)
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


















# data = {
#         "parent": {
#             "database_id": "ffff0618cfa5815e8043d9a775d32835"
#         },
#         "properties": {
#             "Book Name": {
#                 "title": [
#                     {
#                         "text": {
#                             "content": title
#                         }
#                     }
#                 ]
#             },
#             "Price": {
#                 "number": price
#             },
#             "Publisher": {
#                 "rich_text": [
#                     {
#                         "text": {
#                             "content": publisher
#                         }
#                     }
#                 ]
#             },
#             # "Publication Year": {
#             #     "number": publishedDate
#             # },
#
#             "Author": {
#                 "relation": [{"id": author_id} for author_id in author_ids]
#             },
#             "Genre": {
#                 "relation": [{"id": genre_id} for genre_id in genre_ids]
#             },
#             "Total pages": {
#                 "number": page_count
#             },
#             "Language": {
#                 "select": {
#                     "name": language
#                 }
#             },
#             "Book Cover": {
#                 "files": [
#                     {
#                         "name": "Book Cover Image",
#                         "external": {
#                             "url": image
#                         }
#                     }
#                 ]
#             },
#             "Status": {
#                 "status": {
#                     "name": status
#                 }
#             }
#         }
#     }