#!/bin/bash

echo "Recording ... PRess Ctrl+C to stop"
arecord -D plughw:1,0 -q -f cd  -t wav | ffmpeg -loglevel panic -y -i  - -ar 16000 -acodec flac file.flac > /dev/null 2>&1
echo "processing... "
wget -q -U "Mozilla/5.0"  --post-file file.flac --header "Content-Type: audio/x-flac; rate=16000" -o - "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" | cut -d\" -f12 >stt.txt

echo -n "You Said: "
cat stt.txt
rm file.flac > /dev/null 2>&1 

 
#arecord -D plughw:1,0 -r 48000 test.wav

