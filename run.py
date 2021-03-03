'''The app entry point'''

from pathlib import Path
from src.app import DataValidator
import sys
import json


def main():
    if len(sys.argv) < 2 or not Path(Path(sys.argv[1])).exists():
        print('Provide a valid data directory path argument')
        sys.exit()

    dir_path = sys.argv[1]

    # Read in the json file data
    file_path = Path(f'{dir_path}/farm_data.json')
    if not file_path.exists():
        print('farm_data.json does not exist')
        sys.exit()

    farm_data = json.load(open(file_path))
    dv = DataValidator(farm_data)

    # present the validation report
    print('\n---------------------------------')
    print('| HARVEST DATA VALIDATOR REPORT |')
    print('---------------------------------')
    print('\nSubmissions with Duplicate Crop Measurements')
    print('--------------------------------------------')
    print(f'{dv.duplicate_crop_data()}')
    print('\nSubmissions where Dry Weights are greater than Wet Weights')
    print('----------------------------------------------------------')
    print(f'{dv.dry_weight_vs_wet_weight()}')


if __name__ == '__main__':
    main()
