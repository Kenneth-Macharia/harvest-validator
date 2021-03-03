# Harvest Validator CLI App

- This app reviews submitted crop cut data, in order to identify any potential issues.
- Issues checked are:

    1. Multiple measurements for the same crop in a single farm
    2. Submissions where the dry weight measurement exceeds the corresponding wet weight measurement
    3. Submissions where the dry weight is outside the standard deviation of all other submissions for the same crop
    4. Submissions where the GPS coordinates of one farm are within 200 meters of another recorded farm
    5. Submissions where the photo submitted is a duplicate of another photo that was submitted.

## Running tha app
