# C2-Server
# IoT Command Control

This project consists of a simple IoT command control system with a Flask server and a client script. The server registers devices, sends commands to them, and receives check-in status from the devices. The client script registers itself with the server, checks in periodically, and executes received commands.

## Features
- Device registration
- Command sending and receiving
- Periodic check-in from devices
- Command execution on devices

## Setup

### Server

1. Navigate to the `server` directory:
   ```sh
   cd server

2. Install dependencies
   ```sh
   pip install flask
3. Run the server
   ```sh
   python app.py


### Client

  1. Navigate to the 'client' directory:
     ```sh
     cd client
  2. Install dependencies
     ```sh
     pip install -r requirements.txt
  3. Run the client
     ```sh
     python client.py



### Endpoints
### Server Endpoints


1.POST /register: Register a new device.
2.GET /command/<device_id>: Get a command for the specified device.
3.POST /check_in: Check-in a device and report its status.
4.GET /devices: View all registered devices.


### Client Functions
1.register_device(): Registers the device with the server.
2.check_in()       : Sends a check-in request to the server.
3.get_command()    : Retrieves a command from the server.
4.execute_command(command): Executes the received command.

### Notes
Ensure that the 'server' is running before starting the 'client'.
The client periodically checks in with the server and retrieves commands.
Change the port number after each use.
