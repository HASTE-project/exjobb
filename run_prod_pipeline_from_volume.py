import simulator_no_flask

# ** This script should be maintained to work on the production pipeline in the SNIC cloud **

ip = '192.168.1.24'
dir = '/mnt/volume2/testDatasets/0'

hio_config_ben_test_hio_example = {'master_host': ip,
                                   'master_port': 8080,
                                   'container_name': 'benblamey/hio-example:latest',
                                   'container_os': 'ubuntu'}

hio_config_ben_test_haste_example = {'master_host': ip,
                                     'master_port': 8080,
                                     'container_name': 'benblamey/haste-example:latest',
                                     'container_os': 'ubuntu'}

hio_config_hokan = {'master_host': '130.239.81.126',
                    'master_port': 8080,
                    'container_name': 'hakanwie/test:batch_hist2',
                    'container_os': 'ubuntu'}

hio_config_hw_image_proc = {'master_host': ip,
                            'master_port': 8080,
                            'container_name': 'benblamey/haste-image-proc:latest',
                            'container_os': 'ubuntu'}

# get_files(file_path, period, binning, color_channel, send_to_target):
simulator_no_flask.get_files(dir, 0.01, None, None, "yes",
                             hio_config=hio_config_hw_image_proc,
                             stream_id_tag='dummy_set')
