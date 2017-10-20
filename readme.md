[IP Project 1](https://courses.ncsu.edu/csc573/lec/001/wrap/proj1.pdf)

##INSTRUCTIONS TO RUN
1. Download the repository on a linux machine
2. Ensure that the python 2.7 is used
3. Set PYTHONPATH variable to the directory of the downloaded repository. For example, if the repository is at an absolute path “/home/user/IP”, then run the following command on the terminal before running the program.
	<br><br>```PYTHONPATH=’/home/user/IP’```


4. Configure any port or hostname attribute for the peers/server in the $PYTHONPATH/config.json file. The default values would work as well given the ports are available on that machine.
5. There is no interactive mode for the registration server, however it will log the messages it receives and sends on the screen for reference. To run the registration server, fire the following command.
	<br><br>```python $PYTHONPATH/rserver/rserver.py -c $PYTHONPATH/config.json```


6. The peer runs the peer client in an interactive mode and the peer server in a daemon and non interactive mode. Provide an <id> as listed in the config json to select a peer configuration from 6 available configurations. Run the peer client and server by firing the following command.
	<br><br>```python $PYTHONPATH/peer/client.py -c $PYTHONPATH/config.json -i <id>```

7. The interactive mode lists 7 set of options as below.
    1. Register with server
    2. Leave the registration server
    3. Query for peers
    4. Send keep-alive signal to registration server
    5. Get an RFC
    6. View current state of the peer
    0. Exit


8. The first 5 options are as commands of the P2P protocol. The sixth option allows user to view the current state of the peer’s awareness with respect to its assigned cookie, known peers and RFC index. Moreover, each option displays the set of messages exchanged and also shows any changes in the current state of the peer.

## TODO
1. concurrency
2. multi host testing