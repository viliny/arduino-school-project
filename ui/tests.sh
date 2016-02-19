#!/usr/bin/env bash

TIME="$(date +%s)"

./printdb.py
#corr
./ParseStatus.py "humidity=12.3;deviceId=laatikko;lidSwitchOpen=1;temp=45;waterLevelLow=0;batteryStatus=OK;measureTime=$TIME;"
./ParseStatus.py "humidity=83.3;deviceId=laatikko2;lidSwitchOpen=0;temp=125;waterLevelLow=0;batteryStatus=OK;measureTime=$((TIME+55));"
./ParseStatus.py "humidity=93.3;deviceId=laatikko;lidSwitchOpen=0;temp=444;waterLevelLow=1;batteryStatus=Battery;measureTime=$((TIME+60));"
#err
./ParseStatus.py "humidity=AA;;;eId;=laatikko;lidSwi=1;batteryStatus=3;meas=ureTime=123;M"
./ParseStatus.py "humidity=''AA';'';'';'eId;=la'atikko;lidS\"wi=1;batt\"eryStatus=3';mea''s=ureTi'me=.;M"
./ParseStatus.py "humidity=83.3;de'viceId=laatikko2;lidSw'itchOpen=0;\"temp=125;waterLevelL\"ow=0;batteryStatus=OK;measureTime=$((TIME+55));"
#corr
./ParseStatus.py "humidity=1123.3;deviceId=123;lidSwitchOpen=0;temp=-4;waterLevelLow=1;batteryStatus=Battery;measureTime=$((TIME+108));"

#errrs
./ParseStatus.py "humidity=A.3;deviceId=virhe;lidSwitchOpen=0;temp=-4;waterLevelLow=1;batteryStatus=Battery;measureTime=1234;"
./ParseStatus.py "humidity=0;deviceId=virhe2;lidSwitchOpen=0;temp=0xFF;waterLevelLow=1;batteryStatus=Battery;measureTime=1234;"
./ParseStatus.py "humidity=123.3;deviceId=virhe3lidSwitchOpen;temp=-4;waterLevelLow=1;batteryStatus=Battery;measureTime=1234;"
./ParseStatus.py "humidity=1523.3;deviceId=virhe4;lidSwitchOpen=0;temp=-4;waterLevelLow=1;batteryStatus=Battery;measureTime=qrqwe;"
./ParseStatus.py "humidity=1523.3;deviceId=virhe5;lidSwitchOpen=0;waterLevelLow=1;batteryStatus=Battery;measureTime=qrqwe;"
./ParseStatus.py ""

#corrs
./ParseStatus.py "humidity=23.3;deviceId=laatikko3;lidSwitchOpen=0;temp=2;waterLevelLow=0;batteryStatus=OK;measureTime=$((TIME+110));"
./ParseStatus.py "humidity=70.3;deviceId=laatikko3;lidSwitchOpen=1;temp=$((TIME%40));waterLevelLow=1;batteryStatus=OK;measureTime=$((TIME+150));"

echo ""
echo "SELECT * FROM Data:"
./printdb.py
