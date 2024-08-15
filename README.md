# Command line utility for leo's works

The *leo* CLI is a quality of life for some common use case at work

# Requirements

* Python 3
* Pip for installing dependencies (see `requirements.txt`)

# Installation

        pip install -U wheel
        pip3 install "git+ssh://git@github.com/leoshchong/leo-script.git"

* Check out the repo and pick a released version (list tags and pick the latest to avoid checking unfinished changes from master)

        git clone git@github.com:leoshchong/leo-script.git
        git tag -l

* Checkout latest

        git checkout main


* Create a virtual environment using python 3.6 or above:

        cd ~/.virtualenv
        python3 -m venv audco

* Activate the virtual environment
    - On Mac:

            source ~/.virtualenv/audco/bin/activate && eval "$(_AUDCO_COMPLETE=source audco)"
            
            or
            
            source activate

    - To make your life easier in the future you can add this as an alias to your .profile (in Mac):

            alias audco_activate='source ~/.virtualenv/audco/bin/activate && eval "$(_AUDCO_COMPLETE=source audco)"'

  This way you will only need to type `audco_activate` instead of remembering the full path to your environment each time

* Install the dependencies using pip:
  cd <github audco directory>
  pip install -r requirements.txt

* Make "leo-script" available on the command line.

        pip install -e <full_path_to_src_main>

  An example the <full_path_to_src_main> would be: `/Users/myUser/workspace/leo-script/src/main`

# One time configuration

Some of the utilities require access to credentials for calling API's.
Run the setup command and input your develop cert and key as prompted:

    leo setup

The command will setup .leo-cli and .aws/config file
