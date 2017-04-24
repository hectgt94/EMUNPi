#!/bin/sh
#Camera - Video and Audio Connection Settings
MAC='60:E3:27:FE:A2:25'
export RESPONSE_STRING=$(curl -XPOST -H 'Content-Type: application/json' -d '{"method":"passthrough","params":{"requestData":{"command":"GET_EXTRA_INFO","content":0},"deviceId":"FFFFDE8C8D867E29EC642E15FCE34D1D00004492"}}' 'https://use1-wap.tplinkcloud.com/?token=8c585b83-53be92f904af4a6e83f9d1c')

IP=`python - << END

import os
import json
from pprint import pprint

response = json.loads(os.environ['RESPONSE_STRING'])
ip = response["result"]["responseData"]["msg"]["iip"]
print ip

END`

PORT='8080'
USER='admin'
PASS='YWRtaW4xMjM0'
VIDEO_PATH='stream/video/mjpeg'
AUDIO_PATH='stream/audio/mpegmp2'

#Transcoding and Streaming Settings
#Video Resolution
RESOLUTION='640x360'
#Video FPS
FPS='30'
#Video Bitrate
VBR='750k'
#Video Buffer Size
BSIZE='750k'
#Video Quality
QUALITY='veryfast'
#Youtube URL Base for Streaming
YOUTUBE_URL='rtmp://a.rtmp.youtube.com/live2'
#Youtube Streaming Key
YOUTUBE_KEY='9zxz-ms0y-8g6f-aybe'

#Status of Camera network connection
STATUS_VIDEO=$(curl -sL -w "%{http_code}" --max-time 1 "http://$USER:$PASS@$IP:$PORT/$VIDEO_PATH" -o /dev/null)
STATUS_AUDIO=$(curl -sL -w "%{http_code}" --max-time 1 "http://$USER:$PASS@$IP:$PORT/$AUDIO_PATH" -o /dev/null)

echo "Validating video and audio sources..."

if [ $STATUS_VIDEO == 200 ];
  then
    echo "Access to video source validated!"
fi

if [ $STATUS_AUDIO == 200 ];
  then
    echo "Access to audio source validated!"
fi

echo "Starting stream with ffmpeg command, further logs provided by ffmpeg..."

CMD=$(ffmpeg -re -i "http://$USER:$PASS@$IP:$PORT/$VIDEO_PATH" -i "http://$USER:$PASS@$IP:$PORT/$AUDIO_PATH" -vcodec libx264 -preset $QUALITY -vf "format=yuv420p" -maxrate $VBR -bufsize $BSIZE -framerate $FPS -g $(($FPS * 2)) -b:v $VBR -acodec libmp3lame -b:a 128k -ac 2 -ar 44100 -f flv -s $RESOLUTION "$YOUTUBE_URL/$YOUTUBE_KEY")


if [ $STATUS_VIDEO == 200 ] && [ $STATUS_AUDIO == 200 ];
  then
    until $CMD ; do
      echo "Restarting ffmpeg command..."
      export RESPONSE_STRING=$(curl -XPOST -H 'Content-Type: application/json' -d '{"method":"passthrough","params":{"requestData":{"command":"GET_EXTRA_INFO","content":0},"deviceId":"FFFFDE8C8D867E29EC642E15FCE34D1D00004492"}}' 'https://use1-wap.tplinkcloud.com/?token=8c585b83-53be92f904af4a6e83f9d1c')
      IP=`python - << END
import os
import json
from pprint import pprint
response = json.loads(os.environ['RESPONSE_STRING'])
ip = response["result"]["responseData"]["msg"]["iip"]
print ip
END
      sleep 10
    done
fi
