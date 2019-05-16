# Python Chat
This App is based on python Programming  
app contains server and client who can communicate in between with socket interface

Server: is responsible for accept client data and stored it into priority queue and process further along with that he is responsible for sending ack to client.
server accept only 20 connection if you want to increase then add it into simply in .cfg file

Client: client is sending message to server and messages are reading from txt file

Messages are passed between client and server are in encrypted format
Server is maintaing priority queue for client messages 


## Installation

1.Create a python environment. All the dependencies of a project should be ported in a Venv

	virtualenv envname

2.Switch to that environment 

	source path-to-env/envname/bin/activate

PS - Install virtualenvwrapper to make the virtual env process easier

3.Install requirements from `requirement.txt`.

Use the requirement files for each environment to install all the requirements in a single step using `pip install -r requirements.env.txt`

4.Run project for server

	python  socket_server.py

5.Run project client 

	python socket_client.py
	python socket_client_1.py