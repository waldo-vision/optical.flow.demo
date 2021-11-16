# waldo-anticheat
A project that aims to use optical flow and machine learning to visually detect cheating or hacking in video clips from fps games. 
Check out this [video](https://youtu.be/GOI9EkLsUm0) discussing the purpose and vision of WALDO.

# Notes
* This project is still under development. 

## The What
A new market for cheats that are visually indistinguishable to the human eye have lead to a rise in "closet hacking" among streamers and professionals.
This form of cheating is extremely hard to detect. In some cases it is impossible to detect, even with today's most advanced anti-cheat software. 

We will combat this new kind of cheating by creating our own deep learning program to detect this behavior in video clips.

## The How
Because of the advanced technology used, the only reliable way to detect this form of cheating is by observing the cheating behavior directly from the end result- gameplay. Our goal is to analyze the video directly using deep learning to detect if a user is receiving machine assistance.

Phase 1 focuses primarily on humanized aim-assist. Upon completion of phase 1, WALDO's main function will be vindication and clarity to many recent "hackusations."

# Skills needed: 
1. Machine learning / neural networks / AI 
2. Visualizations and graphics 
3. Data analysis 
4. General python 
5. Website design / programming 
6. Game graphics / video analysis 
7. Gamers
8. Current closet hackers you can help ( ͡° ͜ʖ ͡°)


# Use in Container:
Segment is for using code inside a Docker container for better development process that includes all dependencies.
For now you have to manually build it because there are no registry with image for pulling:

1) Enter the Directory with repo and Dockerfile

2) Build an image with command:
*"docker build -t waldo.optical.flow.image ."*

You can also add tag for versioning in the end of the name like this:
*"docker build -t waldo.optical.flow.image:1.0.0 ."*
The default tag is *latest*

3) Create and run container with command:
*"docker run -t -d --name waldo.optical.flow waldo.optical.flow.image"*

The tag that was created in previous step can be used with the image name *waldo.optical.flow.image:1.0.0* and the default is *latest*

In this scenario it will work on background and will not exit because for now there are no process to be working with.

# For container auto building and starting it with working api:
*"docker-compose up -d --build"*

This way you will have automatic docker image building, automatic start of it in background and you will have an api process started on your localhost.
For accessing api use http://127.0.0.1:8000/docs or http://127.0.0.1:8000/recoc

For all custom changing of Docker / docker-compose env variables use *.env* file
For processing env variables to image -> running container - use *var.env* 
