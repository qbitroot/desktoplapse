# desktoplapse
Linux command-line interface tool for recording desktop into a fast-motion `.mp4` video.

# Installation
Firstly, you need Python 3 and `python3-pip`. Then, install ffmpeg (`sudo apt install ffmpeg` for Debian-based GNU/Linux distribution). My script uses ffmpeg for stitching captured frames into one video. Then clone this repository and go to its folder: `git clone https://github.com/gangural/desktoplapse; cd desktoplapse`. Install Python dependencies from requirements file: `sudo pip3 install -r requirements.txt`. That's it!

# Usage
To list all available options, run `python3 desktoplapse.py -h`:

    usage: desktoplapse.py [-h] [-f FPS] [-s SPEED] [-o OUTPUT] [-q QUALITY] [-r REDUCE]
                           [--frame-folder FRAME_FOLDER] [--preserve-frames]

    optional arguments:
      -h, --help            show this help message and exit
      -f FPS, --fps FPS     amount of frames captured per one second (default: 10)
      -s SPEED, --speed SPEED
                            speed up factor (default: 5.0)
      -o OUTPUT, --output OUTPUT
                            location of output video file, default is
                            TIMESTAMP.mp4
      -q QUALITY, --quality QUALITY
                            JPEG quality from 0 to 100 of captured frames
                            (default: 80)
      -r REDUCE, --reduce REDUCE
                            image reduce factor (default: 1.0)
      --frame-folder FRAME_FOLDER
                            path to folder where captured frames are stored
                            (default: cap)
      --preserve-frames     do not delete captured frames

For example, if you want to capture a desktop screen timelapse with 10x speed (10 real seconds = 1 timelapse second) with FPS 20 into a video file named `capture.mp4`, run this command:

`python3 desktoplapse.py --speed 10 --fps 20 --output capture.mp4`

or

`python3 desktoplapse.py -s 10 -f 20 -o capture.mp4`

If `-o/--output` is not specified, a unix timestamp + `.mp4` will set as output video file name. For example, `1592413634.mp4`

While capturing a timelapse, many screenshots are made and saved to `--frame-folder` (`cap` by default). Then they get deleted if `--preserve-frames` option is not set. If `--preserve-frames` is set, you can pause recording and continue later.

If you record a really long timelapse (5+ hours), you can reduce image size twice. To do this, use `-r 2` option.
