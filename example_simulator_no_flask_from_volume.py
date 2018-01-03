import simulator_no_flask
dir = '/mnt/volume2/testDatasets/0'

# This pipeline was for ben to test simulator integration
hio_config_ben_test = {'master_host': '130.239.81.84',
                       'master_port': 8080,
                       'container_name': 'hakanwie/test:batch_hist2',
                       'container_os': 'ubuntu'}

# This is the production pipeline
hio_config_hokan = {'master_host': '130.239.81.126',
                    'master_port': 8080,
                    'container_name': 'hakanwie/test:batch_hist2',
                    'container_os': 'ubuntu'}

simulator_no_flask.get_files(dir, 0.01, 1, ["1"], "yes", hio_config=hio_config_hokan, stream_id_tag='test_set')
