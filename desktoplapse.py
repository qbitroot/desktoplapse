import argparse
import datetime
import os
import sys
from time import sleep

from PIL import Image, ImageDraw
from Xlib import X, display

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--fps", type=int, default=10,
				help="number of frames captured per second (default: %(default)s)")
parser.add_argument('-s', "--speed", type=float, default=5.0, help="speed up factor (default: %(default)s)")
parser.add_argument('-o', "--output", help="location of output video file, default is TIMESTAMP.mp4")
parser.add_argument('-q', "--quality", type=int, default=80,
				help="JPEG quality from 0 to 100 of captured frames (default: %(default)s)")
parser.add_argument('-r', "--reduce", type=float, default=1.0,
		    		help="screenshot size scale down factor (default: %(default)s)")
parser.add_argument("--frame-folder", default='cap',
				help="path to folder where captured frames are stored (default: %(default)s)")
parser.add_argument("--preserve-frames", action='store_true', help="do not delete captured frames")
args = parser.parse_args()


def ask(question, default=False):
	y, n = 'y', 'n'
	if default:
		y = 'Y'
	else:
		n = 'N'
	answer = input(f'{question} [{y}/{n}]? ')
	if not answer or (answer[0] == 'y') == default:  # default option
		return default
	else:
		return not default


fps = args.fps
speed = args.speed

delay = speed / fps

if len(sys.argv) < 2:
	print("Warning: you used default options. To view available arguments, use -h or --help flag.")

if not os.path.exists(args.frame_folder):
	os.mkdir(args.frame_folder)
	print(f"Created {args.frame_folder} folder")

print(f"Delay: {delay} seconds")

if delay < 0.2:
	print("Warning: possible performance degradation because of too small delay. Increasing --speed or decreasing --fps highly recommended.")
	if not ask("Proceed to recording"):
		print("Exiting...")
		sys.exit(0)

print("Press Ctrl+C to stop recording")

d = display.Display()
r = d.screen().root
geometry = r.get_geometry()
w, h = geometry.width, geometry.height

try:  # attempt to continue recording
	i = int(max([f.split('.')[0] for f in os.listdir(args.frame_folder)])) + 1
except:
	i = 0

try:
	while True:
		raw = r.get_image(0, 0, w, h, X.ZPixmap, 2 ** 32 - 1).data
		img = Image.frombytes('RGB', (w, h), raw, 'raw', 'BGRX')
		filename = f'{str(i).rjust(6, "0")}.jpg'
		if not args.reduce == 1:
			img = img.resize((int(w // args.reduce), int(h // args.reduce)))
		td = str(datetime.timedelta(seconds=(i / fps)))
		td = td[:-3] if '.' in td else td + '.000'
		img.save(os.path.join(args.frame_folder, filename), quality=args.quality)
		print(f'[{td}] Saved to {filename}')
		i += 1
		sleep(delay)
except KeyboardInterrupt:
	if args.preserve_frames and not ask("\nStitch video"):
		print("OK, exiting...")
		sys.exit(0)
	print("\nStarting stitch.sh script...")
	stitch_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stitch.sh')
	if args.output:
		os.system(f'bash {stitch_path} {fps} {args.output}')
	else:
		os.system(f'bash {stitch_path} {fps}')  # bash script will generate timestamp
	if not args.preserve_frames:
		os.system(f'rm {args.frame_folder}/*.jpg')
		print("Removed jpg frames!")
