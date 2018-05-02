# omega
Programs and info on the Onion Omega/Omega2 IoT chip

#sparkRun.py
The file sparkRun.py will connect an OmegaII to a Cisco Spark room and allow you to use the room as a command and control server. 

Usage:

    root@onion1:~# ./sparkRun.py --help | sed 's/^/    /'
    usage: sparkRun.py [-h] [--pid] [--delay DELAY] [--log] [--config CONFIG]
    
    A program to receive messages from Cisco Spark on Omega
    
    optional arguments:
      -h, --help       show this help message and exit
      --pid            Create a pid file in /var/run/sparkRun.pid
      --delay DELAY    Number of seconds to wait between readings, default 30
      --log            Create a log file in /tmp/sparkRun.log
      --config CONFIG  Specify an alternate location of the config file, default
                       ./spark.cfg

To run commands type: run command i.e. run df -h 

To update the Omega OLED Shield if you have one, type oled "My Message Here" 
