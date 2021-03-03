'''The harvest data validator module'''


class DataValidator:
    '''This class indentifies issues in a provided json data set'''

    def __init__(self, data):
        self.input = data['harvest_measurements']

    def duplicate_crop_data(self):
        '''This method checks for multiple measurements for the same crop
         in a single farm'''

        seen, output = {}, {}

        for farm in self.input:
            # Check if a particular farm has been previosly parsed
            if farm['farm_id'] not in seen.keys():
                seen[farm['farm_id']] = farm['crop']
            else:
                # If a farm has already been encountered, check if for this
                # crop occurence
                if seen[farm['farm_id']] == farm['crop'] and farm['farm_id'] \
                        not in output:
                    output[f'farm_id: {farm["farm_id"]}'] = \
                        f'duplicate crop: {farm["crop"]}'

        return output if output else None

    def dry_weight_vs_wet_weight(self):
        '''This method checks whether dry weight measurement exceeds
         the corresponding wet weight measurement'''

        output = {}

        for farm in self.input:
            if farm['dry_weight'] > farm['wet_weight']:
                output[farm["farm_id"]] = farm["crop"]

        return output if output else None

    def dry_weight_std_deviation(self):
        '''This method checks whether the dry weight is outside the
        standard deviation of all other submissions for the same crop'''
        pass

    def location_check(self):
        '''This method checks whether the GPS coordinates of one farm are
        within 200 meters of another recorded farm'''
        pass

    def duplicate_photo_data(self):
        '''This method checks for duplicate photo submissions'''
        pass
