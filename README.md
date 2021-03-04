# Harvest Validator CLI App

- This app reviews submitted crop cut data, in order to identify any potential issues.
- Issues checked are:

    1. Multiple measurements for the same crop in a single farm
    2. Submissions where the dry weight measurement exceeds the corresponding wet weight measurement
    3. Submissions where the dry weight is outside the standard deviation of all other submissions for the same crop
    4. Submissions where the GPS coordinates of one farm are within 200 meters of another recorded farm
    5. Submissions where the photo submitted is a duplicate of another photo that was submitted.

## How to run the app

1. Clone this repo on a machine which has python and git installed

    `git clone https://github.com/Kenneth-Macharia/harvest-validator.git`

2. Navigate into the `harvest_validator` folder downloaded and create a virtual environment to isolate the application

    `cd /{path_to_harvest_validator}/harvest_validator`

    `python -m venv {name_of_your_virtualenv}`

3. Activate the virtual environment and install the app dependancies

    Unix: `source ./{name_of_your_virtualenv}/bin/activate`

    Windows: `source ./{name_of_your_virtualenv}/Scripts/activate`

    `pip install -r requirements.txt`

4. Run the app passing the path to the `harvest_data_set` folder as an argument. This
  folder contained within the repo folder, contains the app test data:

    `python run.py ./harvest_data_set`
