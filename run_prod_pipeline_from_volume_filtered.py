import simulator_no_flask

# ** This script should be maintained to work on the production pipeline in the SNIC cloud **


ip = '192.168.1.24'
dir = '/mnt/ImageDataV2/fromAl/Data_20151215 HepG2 LNP size exp live cell 24h_20151215_110422/AssayPlate_NUNC_#165305-1'
WELLS_FOR_ONLINE_ANALYSIS = ['B05', 'C02', 'C03', 'C04', 'C09', 'D04', 'D06', 'E10', 'F09', 'G02', 'G10', 'G11']

SEND_ONLY_FILES = lambda file_info: file_info['imaging_point_number'] == 1 \
                                    and file_info['well'] in WELLS_FOR_ONLINE_ANALYSIS

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
                                             stream_id_tag='from_al',
                                             send_matching_files=SEND_ONLY_FILES
                                             )

    return stream_id


if __name__ == '__main__':
    run()
