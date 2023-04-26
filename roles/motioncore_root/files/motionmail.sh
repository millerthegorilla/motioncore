#!/bin/bash

MOTION_FILE_NAME=$(basename ${1});

/usr/bin/podman unshare chown 1000:1000 -R ./files;
/usr/bin/podman run -it --name python_motion --user 1000 -v /var/home/motion_user/files:/var/home/motioncore/motion_files:Z -e MOTION_FILE_PATH="/var/home/motioncore/motion_files/${MOTION_FILE_NAME}" -e MOTION_EMAIL_USERNAME="jamesstewartmiller@gmail.com" -e MOTION_EMAIL_PORT="465" -e MOTION_EMAIL_HOST="smtp.gmail.com" -e MOTION_EMAIL_SENDER="MotionCoreCamera@gmail.com" -e MOTION_EMAIL_RECEIVER="jamesstewartmiller@gmail.com" --secret motion_email_secret,type=env,target=MOTION_EMAIL_PASS python:motioncore 2>&1 >> /var/log/custom_motion.log;
/usr/bin/podman rm python_motion;
/usr/bin/podman unshare chown root:root -R ./files;