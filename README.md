# Command line utility for leo's works

The *leo* CLI is a quality of life for some common use case at work

# Requirements

* Python 3
* Pip for installing dependencies (see `requirements.txt`)

# Installation

    pip3 install -U wheel
    pip3 install "git+ssh://git@github.com/leoshchong/leo-script.git"

# One time configuration

Some of the utilities require access to credentials for calling API's.
Run the setup command and input your develop cert and key as prompted:

    leo setup

The command will setup .leo-cli and .aws/config file. Example:

    Key []: /Users/user/cert/mykey.key
    Cert []: /Users/user/cert/mycert.crt
    Email []: my_email@test.co.uk
    
# Development

* Make "leo-script" available on the command line.

      pip install -e <path_to_setup>

  An example the <path_to_setup> would be: `/Users/myUser/workspace/leo-script/` or just `.`


