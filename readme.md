[IP Lab HW1](https://courses.ncsu.edu/csc573/lec/001/wrap/proj1.pdf)

export PYTHONPATH='../'

##Run rserver
python rserver.py -c ../config.json -d

##Run client
python client.py -c ../config.json -i 1 -d

##TODO
RFC Server should spawn a thread to serve
contact rs if rfc not present locally to get list of peers
1. contact one peer for rfc index,
2. merge it with its own,
4. search for the rfc
4. Download from respective peer
then repeat one if failed until the list exhausts or rfc found.

uniqueness of peers in the peerlist






create an instrutions file to run the program