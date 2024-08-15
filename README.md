# Command line utility for leo's works

The *leo* CLI is a quality of life for some common use case at work

# Requirements

* Python 3
* Pip for installing dependencies (see `requirements.txt`)

# Installation

        pip3 install -U wheel
        pip3 install "git+ssh://git@github.com/leoshchong/leo-script.git"

# Development

* Make "leo-script" available on the command line.

        pip install -e <full_path_to_src_main>

  An example the <full_path_to_src_main> would be: `/Users/myUser/workspace/leo-script/src/main`

# One time configuration

Some of the utilities require access to credentials for calling API's.
Run the setup command and input your develop cert and key as prompted:

    leo setup

The command will setup .leo-cli and .aws/config file
