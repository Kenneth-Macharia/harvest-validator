'''The application entry point'''

from pathlib import Path
from sys import argv, exit
from json import load
from src.validator import DataValidator


def main():
    if len(argv) < 2 or not Path(argv[1]).exists():
        exit('''Invalid directory path:
        Usage: | python run.py <valid_folder_path> | e.g /usr/bin
        ''')

    dir_path = argv[1]

    # Read in the json file data
    file_path = Path(f'{dir_path}/farm_data.json')
    if not file_path.exists():
        exit('File Not Found: farm_data.json does not exist')

    farm_data = load(open(file_path))

    # Read in image name list
    image_list = [p.name for p in Path(dir_path).glob('*.jpg')]

    if not image_list:
        exit('Files Not Found: Valid image files (.jpg) not found in provided data directory')

    # Initialize validator module
    dv = DataValidator(farm_data, image_list, dir_path)

    # Render the validation report
    print('\n---------------------------------')
    print('| HARVEST DATA VALIDATOR REPORT |')
    print('---------------------------------')
    print('\nSubmissions with Multiple Crop Measurements')
    print('-------------------------------------------')
    print(f'{dv.duplicate_crop_data()}')
    print('\nSubmissions where Dry Weights are greater than Wet Weights')
    print('----------------------------------------------------------')
    print(f'{dv.dry_weight_vs_wet_weight()}')
    print('\nSubmissions where Dry Weights are outside the Standard Deviation')
    print('----------------------------------------------------------------')
    print(f'{dv.dry_weight_std_deviation()}')
    print('\nSubmissions where GPS Coords are within 200 Meters')
    print('--------------------------------------------------')
    print(f'{dv.location_check()}')
    print('\nSubmissions with Duplicate Photos')
    print('---------------------------------')
    print(f'{dv.duplicate_photo_data()}\n')
    print('********** End of Report *********\n')


if __name__ == '__main__':
    main()
