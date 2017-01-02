# zero-static
Serve ZeroNet Zites (almost) like normal ones. Edit

**IMPORTANT: This project isn't finished yet and might be very insecure**

# How To
First clone ZeroNet: `git clone https://github.com/HelloZeroNet/ZeroNet`

Then run the Build script: `bash build.sh yoursite.bit pack cleanbuild` (This generates a `ZeroStatic.tar.gz`)

Prepare the machine to use: `apt install python python-dev python-pip` and `pip install msgpack-python gevent`

Now just extract the tar: `mkdir -p ZeroStatic;tar xvfz ../ZeroStatic.tar.gz`

And run `bash start.sh`

# Debugging
To debug just run: `bash build.sh yoursite.bit debug`
