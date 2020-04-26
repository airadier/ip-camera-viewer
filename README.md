# IP Camera JPEG visualizer

A very basic IP camera visualizer.

![Capture](doc/capture.png)


In my setup, I have an IP camera at home, and a script that is run every second to capture an image like:

```
curl -s http://user:pass@http://ip-camera/snapshot.cgi > cam-$(date +%Y%m%d-%H%M%S.%6N).jpg
```

This script, run every second via watch, creates a cam-YYYYmmdd-HHMMSS.ffffff.jpg file, with a millisecond timestamp.

These files are created in a SSHFS folder mounted remotely on a cloud server, so they are synced in real time.

This simple visualizer takes the pictures from that folder, and by defining folder and pattern, allows visualization in real-time (refresh once per second) with a small delay of 3 seconds to allow the pictures to be fully uploaded. Some simple controls allow to change the time frame, and jump back and forward.

It works with a simple backend flask application that servers the view.html template. This template uses javascript to refresh a canvas, requesting an image every second, from current (now) timestamp. A 'delta' is added to the requested timestamp, and the delta can be modified via some control buttons.

The backend receives the requested timestamp, and searches for the image with the nearest timestamp, then servers it.
