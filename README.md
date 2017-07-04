node-red-contrib-vokaturi
==============================
<a href="http://nodered.org" target="_new">Node-RED</a> node that exploits the <a href="http://nodered.org" target="_new">Vokaturi</a> library to provide batch emotion analysis of a WAV file.
It depends on the Vokaturi library ( version 2-1b)
Tested on Linux and MacOS

Install
-------
Run the following command in your Node-RED user directory - typically `~/.node-red`

        npm install node-red-contrib-vokaturi

Prerequisites
------------
The python module requires <a href="https://www.scipy.org/install.html">scify</a>

Libraries
------------
It uses OpenVokaturi 2.1b

Usage
-----
The node takes a path as argument of the wav file to be analysed; internally it calls a python scripts that uses the openvokaturi facilities
