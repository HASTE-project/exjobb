import re

# Parse Filenames for AstraZeneca dataset:

__pattern = re.compile('^([0-9]+)?'  # Docs states this should be part of Plate ID, but looks like an additional image seq. number field?
                       + '(.+)_'  # Plate ID
                       + '([A-Za-z]+[0-9]+)_'  # Well
                       + 'T([0-9]{4})+'  # tpIndex
                       + 'F([0-9]{3})+'  # fpIndex
                       + 'L([0-9]{2})+'  # tlIndex
                       + 'A([0-9]{2})+'  # alIndex
                       + 'Z([0-9]{2})+'  # zpIndex
                       + 'C([0-9]{2})+'  # chIndex
                       + '(\.tiff?)?',
                       re.IGNORECASE)  # Windows has case-insensitive filenames


def parse_azn_file_name(filename):
    # Note: this is for parsing file NAMES not file PATHS.

    match = re.search(__pattern, filename)

    if match is None:
        return None

    metadata = {
        'assay_plate_name': match.group(2),
        'well': match.group(3).upper(),  # e.g. A1, H12
        'time_point_number': int(match.group(4)),  # 0001 to 9999
        'imaging_point_number': int(match.group(5)),  # 001 to 999
        'time_line_number': int(match.group(6)),  # 0001 to 9999
        'action_list_number': int(match.group(7)),  # 0001 to 9999
        'z_index_3d': int(match.group(8)),  # 01 to 99
        'color_channel': int(match.group(9)),  # 01 to 99  # TODO: convert this to 'red' etc.?
        # channel 1 is the red / orange channel with LNP particles,
        # Channel 2 is the green channel with the GFP expression and
        # channel 3 is a bright field channel where you see the cells.
        # Channel 4 is a failed staining only showing dead cells or cells not stuck to the bottom of the well
    }

    if match.group(1) is not None:
        metadata['image_sequence_number'] = int(match.group(1))

    return metadata


if __name__ == '__main__':
    names = [
        '0101AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01.tif',
        '0101AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01.tiff',
        '0101AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01.bmp',
        '0101AssayPlate_NUNC_#165305-1_F05_T0038F002L01A02Z01C01']

    golden_metadata = {
        'image_sequence_number': 101,
        'assay_plate_name': 'AssayPlate_NUNC_#165305-1',
        'well': 'F05',
        'time_point_number': 38,
        'imaging_point_number': 2,
        'time_line_number': 1,
        'action_list_number': 2,
        'z_index_3d': 1,
        'color_channel': 1}

    for name in names:
        metadata = parse_azn_file_name(name)
        print(metadata)

        if golden_metadata != metadata:
            raise Exception('golden metadata does not match!')
        else:
            print('metadata is match!')
