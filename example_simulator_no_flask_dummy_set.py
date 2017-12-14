import simulator_no_flask
dir = './test-images'

# get_files(file_path, period, binning, color_channel, send_to_target):
simulator_no_flask.get_files(dir, 0.01, 1, ["1"], "yes")