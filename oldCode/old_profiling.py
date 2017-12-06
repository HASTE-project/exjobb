def timer(file_path):
    json_file = open(file_path, "r")
    run_information = json_file.read()
    json_file.close()
    run_information = json.loads(run_information)

    for run in run_information:
        frequency = run_information[run]['frequency']
        color_channel = run_information[run]['color_channel']
        binning = run_information[run]['binning']
        file_path = run_information[run]['file_path']
        connect_kafka = run_information[run]['connect_kafka']
        result = time_get_files(file_path, frequency, binning, color_channel, connect_kafka)
        save_as_csv(result, run)