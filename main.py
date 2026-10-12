import requests
from typing import Any

def fetch_users(api_url : str) -> list | dict | Any:
    try:
        # Notify ongoing api connection
        print("Connecting to JSONPlaceholder...")
        # retrieve the user data from the api endpoint
        response = requests.get(api_url, timeout=5)
        # check if it was successful
        response.raise_for_status()
        parsed = response.json()
        print(f"Successfully retrieved {len(parsed)} users!")
        # return the json parsed response
        return parsed
    except requests.exceptions.Timeout as timeout:
        print(f"Request timed out: {timeout}")
    except requests.exceptions.RequestException as e:
        print(f"Failed request: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    except Exception as e:
        print(f"{e}")
        raise Exception

def process_users(users: list) -> list:
    if not users:
        print("No users were found.")
        return []
    
    new_users = []
    for user in users:
        if "address" not in users or "city" not in users["address"]:
            print("User has no address or city.")
            new_users.append({
                "name" : user["name"],
                "username" : user["username"],
                "email" : user["email"]
            })

        new_users.append({
            "name" : user["name"],
            "username" : user["username"],
            "email" : user["email"],
            "city" : user["address"]["city"]
        })

    return new_users

def display_users(users: list) -> None:
    header = "=================================\n        API USER FETCHER        \n================================="
    print(header)

    for index, user in enumerate(users):
        user_header = f"---------------------------\nUser #{index + 1}\n---------------------------"
        print(user_header)
        for text in ["Name", "Username", "Email", "City"]:
            num_spaces = 15 - len(text)
            info_text = f"{text}: {" " * num_spaces}{user[text.lower()]}"
            print(info_text)

    footer = f"=================================\nTotal users retrieved: {len(users)}\n================================="
    print(footer)

def main():
    api_endpoint = "https://jsonplaceholder.typicode.com/users"
    users = fetch_users(api_endpoint)
    processed = process_users(users)
    display_users(processed)

if __name__ == "__main__":
    main()