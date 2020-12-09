# App
## Installing Python
* Windows
  * https://realpython.com/installing-python/#how-to-install-python-on-windows
* MacOS
  * https://realpython.com/installing-python/#how-to-install-python-on-macos
* On MacOS, a version of Python 2 may be the default when typing `python` in the command line.  If this is the case, then replace all instances of `python` with `python3`

## Installing Packages
* First, create a virtual environment with `python -m venv <name of virtual environment>`
  * `<name of virtual environment>` can be replaced with anything, such as `venv`
* Activate the virtual environment
  * `source <name of virtual environment>/bin/activate`
  * `(venv)` should appear on your command prompt line
* Next, install all of the required packages
  * `pip install -r requirements.txt`
  * You can check that the packages were all installed by typing `pip list`

## Running the App
* Terminal
* Standard
