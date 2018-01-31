import simulator_no_flask

# ** This script should be maintained to work on the production pipeline in the SNIC cloud **

ip = '192.168.1.24'
dir = '/mnt/ImageData/testDatasets/0'

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

hio_config_hw_image_proc_profiling = {'master_host': ip,
                                      'master_port': 8080,
                                      'container_name': 'benblamey/haste-image-proc:latest-profiling',
                                      'container_os': 'ubuntu'}


def run():
    # get_files(file_path, period, binning, color_channel, send_to_target):
    stream_id = simulator_no_flask.get_files(dir, 0, None, None, "yes",
                                             hio_config=hio_config_hw_image_proc,
                                             stream_id_tag='test_dataset_0')

    return stream_id


if __name__ == '__main__':
    run()
