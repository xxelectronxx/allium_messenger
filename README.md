# Alium Messenger
A private messenger.
The plan is to create a messenger that is reasonably private, using the Tor network, for practice.


# System Setup
1) Basic developement tools need to be installed on your system. You probably need superuser access for this.
    
    For Linux:
    ```
    sudo apt update
    sudo apt install build-essential
    sudo apt install python3-dev
    ```
    Mac likely has the required tools already. If not, simply go to the next section to see what is missing, if anything.
1) Clone this repository
    
    ```
    cd
    mkdir git
    cd git
    git clone git@github.com:xxelectronxx/alium_messenger.git
    cd alium_messenger
    ```
1) Virtualenv
    ```
    python3 -m venv --without-pip venv
    source venv/bin/activate
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm get-pip.py 
    pip install -U pip
    deactivate
    ```
1) Install PyCharm
    On linux simply do:
    ```
    sudo snap install pycharm-community --classic
    ```
     
    On Mac, download from [the PyCharm site](https://www.jetbrains.com/pycharm/) and install.