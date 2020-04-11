import vapoursynth as vs
import sys
import os
import havsfunc as haf
import mvsfunc as mvf
import muvsfunc as muf

core = vs.get_core(threads = 4)

core.max_cache_size = 6000

a = "00002.m2ts"
src8 = core.lsmas.LWLibavSource(a)
src_y = core.resize.Point(src8, format=vs.GRAYS)

# params here
frame_num = src_y.num_frames // 3 # Frame number to be tested.
stepping = 12 # Stepping of height.
min_height = 500 # Auto-adjusted based on stepping.
max_height = 1000 # Auto-adjusted based on stepping.
clear_png = True # Set to False to disable auto deleting pngs.
# end params zone

if clear_png:
	files_in_directory = os.listdir('.\\')
	filtered_files = [file for file in files_in_directory if file.endswith(".png")]
	for file in filtered_files:
		os.remove(file)

clip = src_y[frame_num]
low_end = min_height // stepping * stepping
high_end = ((max_height - 1) // stepping + 1) * stepping + 1
height_range = range(low_end, high_end, stepping)

scalers = [
	["Bilinear"], ["Bicubic", 1/3, 1/3], ["Bicubic", 0, 0.5], ["Bicubic", 0.5, 0.5],
	["Lanczos", 2], ["Lanczos", 3], ["Lanczos", 4], 
	["Spline16"], ["Spline36"]
]

last = core.std.Splice([muf.getnative(clip, tuple(height_range), *args) for args in scalers])
last.set_output()


