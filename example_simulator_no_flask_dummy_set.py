import simulator_no_flask

ip = '130.238.89.140'

dir = './test-images'

# This pipeline was for ben to test simulator integration
hio_config_ben_test_hio_example = {'master_host': ip,
                                   'master_port': 8080,
                                   'container_name': 'benblamey/hio-example:latest',
                                   'container_os': 'ubuntu'}

# This pipeline was for ben to test simulator integration
hio_config_ben_test_haste_example = {'master_host': ip,
                                     'master_port': 8080,
                                     'container_name': 'benblamey/haste-example:latest',
                                     'container_os': 'ubuntu'}

# This is the production pipeline
hio_config_hokan = {'master_host': '130.239.81.126',
                    'master_port': 8080,
                    'container_name': 'hakanwie/test:batch_hist2',
                    'container_os': 'ubuntu'}

# get_files(file_path, period, binning, color_channel, send_to_target):
simulator_no_flask.get_files(dir, 0.01, None, None, "yes",
                             hio_config=hio_config_ben_test_haste_example,
                             stream_id_tag='dummy_set')
