# workspace
To be used as a submodule to CustoPiZer. It's safe to delete.

run.py is the main script. Pulls the latest octopi release image, renames it to input.img
and then starts the docker command to convert it to an output.img that can be used to flash to the rasppi.

To use it, runL pip install -r requirements.txt first.
I've used this in ubuntu 20.04 with docker & unzip installed.
