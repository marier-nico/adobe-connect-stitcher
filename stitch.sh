#!/bin/bash

# This doesn't quite work, but it is tested with the class ID : ppyfytvrxa4t

#for screenshare in screenshare_*.flv; do
#    ffmpeg -i "$screenshare" -s 1920x1080 "$screenshare".mkv
#done

# This should be the exact length between the videos (may need more for more videos)
# -> start_2 - (start_1 + duration_1) = space_between
ffmpeg -t 00:04:11 -s 1920x1080 -f rawvideo -r 1 -i /dev/zero empty.mkv

cat > videos.txt << EOF
file 'screenshare_1_3.flv.mkv'
file 'empty.mkv'
file 'screenshare_3_6.flv.mkv'
EOF

ffmpeg -f concat -safe 0 -i videos.txt -c copy all_videos.mkv

ffmpeg -i cameraVoip_0_2.flv -i cameraVoip_0_4.flv -i cameraVoip_2_5.flv -i cameraVoip_2_7.flv -i cameraVoip_2_8.flv \
    -itsoffset 00:04:25 -i all_videos.mkv \
    -filter_complex "[1]adelay=540s|540s[s1]; \
                     [2]adelay=800s|800s[s2]; \
                     [3]adelay=2263s|2263s[s3]; \
                     [4]adelay=5019s|5019s[s4]; \
                     [0][s1][s2][s3][s4]amix=inputs=5[mixout]" \
    -map "[mixout]":a -map 5:v -c:v copy final_output.mkv

