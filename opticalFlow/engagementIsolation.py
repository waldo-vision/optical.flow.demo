#!/usr/bin/env python3
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import cv2
import sys, os


class Isolator:
	def __init__(self, file_path, out_dir, clip_length=120):
		self.file_path = file_path
		self.file_name = file_path.split(os.path.sep)[-1]
		self.clip_length = clip_length
		self.out_dir = out_dir
		self.video = VideoFileClip(file_path)


	def _cleanup_file(self, path):
			print("cleaning up file: " + path)
			os.remove(path)

	def get_frames(self):
		video = cv2.VideoCapture(self.file_path)
		while video.isOpened():
			rete, frame = video.read()
			if rete:
				yield frame
			else:
				break
		video.release()
		yield None

	def center_crop(self, img, width, height):
		crop_width = width if width < img.shape[1] else img.shape[1]
		crop_height = height if height < img.shape[0] else img.shape[0]

		mid_x, mid_y = int(img.shape[1]/2), int(img.shape[0]/2)
		cw2, ch2 = int(crop_width/2), int(crop_height/2)
		return img[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]

	def new_clip(self, clip_counter, size):
		return cv2.VideoWriter(self.clip_name(clip_counter), 
			cv2.VideoWriter_fourcc(*'mp4v'), 15 , size)

	def clip_name(self, clip_counter):
		return self.out_dir + os.path.sep + self.file_name.split('.')[0] + '_' + str(clip_counter) + '_engagement.mp4'

	def parse_video(self, crop_width, crop_height):
		clip_counter = 0
		recording = 0
		wrote_on_prev_frame = False
		video_out = None
		clips = {}

		counter = 0
		for frame in self.get_frames():
			if frame is None:
				break
			counter += 1
			frame = self.center_crop(frame, crop_width, crop_height)
			frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

			#HOGDescriptor to identify People in an image
			#Better detectors may be selected in order to parse out when an enemy is near a player's crosshair
			#Or to identify whenever a player is shooting
			hog = cv2.HOGDescriptor()
			hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
			(humans, confd) = hog.detectMultiScale(frame,
				winStride=(4,4),
				padding=(8,8),
				scale=1.005
				)



			for i in range(0, len(humans)):
				if confd[i] > 1.0:
					recording = self.clip_length
					if not wrote_on_prev_frame:
						clip_counter += 1
						clips[self.clip_name(clip_counter)] = {
							"start": counter
						}
						
			if recording > 0:
				recording -= 1
				wrote_on_prev_frame = True
			elif wrote_on_prev_frame:
				clips[self.clip_name(clip_counter)]["end"] = counter
				wrote_on_prev_frame = False

		if clips[self.clip_name(clip_counter)]["end"] is None:
			clips[self.clip_name(clip_counter)]["end"] = counter
		return clips


	def cut_clips(self, clips):
		for file_name in clips:
			clip = clips[file_name]
			ffmpeg_extract_subclip(self.file_path, int(clip["start"] / self.video.fps), int(clip["end"]/ self.video.fps), targetname=file_name)






def main():
	print("Running main")
	iso = Isolator(sys.argv[1], sys.argv[2], 240)
	iso.cut_clips(iso.parse_video(200, 200))


if __name__ == "__main__":
	main()
