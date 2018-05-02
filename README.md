# omega
Programs and info on the Onion Omega/Omega2 IoT chip

#sparkRun.py
The file sparkRun.py will connect an OmegaII to a Cisco Spark room and allow you to use the room as a command and control server. 

Usage:

    root@onion1:~# ./sparkRun.py --help 
    usage: sparkRun.py [-h] [--pid] [--delay DELAY] [--log] [--config CONFIG]
    
    A program to receive messages from Cisco Spark on Omega
    
    optional arguments:
      -h, --help       show this help message and exit
      --pid            Create a pid file in /var/run/sparkRun.pid
      --delay DELAY    Number of seconds to wait between readings, default 30
      --log            Create a log file in /tmp/sparkRun.log
      --config CONFIG  Specify an alternate location of the config file, default
                       ./spark.cfg

To enable logging:

    root@onion1:~# ./sparkRun.py --log
    root@onion1:~# head  /tmp/sparkRun.log  
    DEBUG:root:2018-05-01 22:46:19.266258:  Started App
    DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.ciscospark.com
    DEBUG:urllib3.connectionpool:https://api.ciscospark.com:443 "GET /v1/rooms HTTP/1.1" 200 None
    DEBUG:root:2018-05-01 22:48:39.735091:  Started App
    DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): api.ciscospark.com
    DEBUG:urllib3.connectionpool:https://api.ciscospark.com:443 "GET /v1/rooms HTTP/1.1" 200 None
    DEBUG:root:2018-05-01 22:48:40.809464:Connected to Spark Room : ...
    DEBUG:urllib3.connectionpool:https://api.ciscospark.com:443 "GET /v1/messages?roomId=...  HTTP/1.1" 200 None
    DEBUG:root:2018-05-02 04:47:11: Received Message: run df -h 
    DEBUG:urllib3.connectionpool:https://api.ciscospark.com:443 "POST /v1/messages HTTP/1.1" 200 None

To run commands type: run command i.e. run df -h 

To update the Omega OLED Shield if you have one, type oled "My Message Here" 
