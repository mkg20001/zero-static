# zero-static
Serve ZeroNet Zites (almost) like normal ones.

**IMPORTANT: This project isn't finished yet and might be very insecure**

# How To
First install `git` so the script can clone ZeroNet

Then run the Build script: `bash build.sh yoursite.bit pack cleanbuild` (This generates a `ZeroStatic.tar.gz`)

Prepare the machine to use: `apt install python python-dev python-pip` and `pip install msgpack-python gevent`

Now just extract the tar: `mkdir -p ZeroStatic && cd ZeroStatic && tar xvfz ../ZeroStatic.tar.gz`

And run `bash start.sh`

# Apache2
There is an Apache2 example config in `zerostatic-apache.conf`

# Debugging
To debug just run: `bash build.sh yoursite.bit debug`
