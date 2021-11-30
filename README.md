# Alium Messenger
A private messenger.
The plan is to create a messenger that is reasonably private, using the Tor network, for practice.


# System Requirements
Basic developement tools need to be installed on your system. You probably need superuser access for this.

For Linux:

    sudo apt-get update
    sudo apt-get install build-essential
    sudo apt-get install python3-dev
  
Mac likely has the required tools already. If not, simply go to the next section to see what is missing, if anything.


# Basic Virtualenv

    python3 -m venv --without-pip venv
    source venv/bin/activate
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm get-pip.py 
    pip install -U pip
    deactivate
