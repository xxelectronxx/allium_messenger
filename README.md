# Allium Messenger
A private messenger.
The plan is to create a messenger that is reasonably private, using the Tor network, for practice.


# System Setup
1) Basic developement tools need to be installed on your system. You probably need superuser access for this.
    
    For Linux:
    ```
    sudo apt update
    sudo apt install build-essential
    sudo apt install python3-dev
    sudo apt install tor
    sudo apt install xclip
    ```
    Mac likely has the required tools already. If not, simply go to the next section to see what is missing, if anything.

2) Adjust Tor settings
    In `/et/tor/torrc` uncomment lines
    ```
    SocksPort 9050
    CntrolPort 9051
    ```

    In command line, run the command below
    ```
    tor --hash-password 'test_password'
    ```
    Copy the result. Modify the line `HashedControlPassword` in the `/etc/tor/torrc` file by replacing the hash with 
    the one you copied.
    
    Restart Tor service by typing the following into the terminal
    ```
    sudo service tor restart
    ```

4) Clone this repository
    
    ```
    cd
    mkdir git
    cd git
    git clone git@github.com:xxelectronxx/allium_messenger.git
    cd allium_messenger
    ```
5) Virtualenv
    ```
    python3 -m venv --without-pip venv
    source venv/bin/activate
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    rm get-pip.py 
    pip install -U pip
    pip install -r requirements.txt
    deactivate
    ```
6) Install PyCharm (for development)
    On linux simply do:
    ```
    sudo snap install pycharm-community --classic
    ```
     
    On Mac, download from [the PyCharm site](https://www.jetbrains.com/pycharm/) and install.

7) 