'''The harvest data validator module'''

from statistics import stdev, mean


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
                    output[farm["farm_id"]] = farm["crop"]

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

        crop_data, output = {}, {}

        for farm in self.input:
            crop_data.setdefault(
                farm['crop'],
                DataValidator.crop_data_agg(self.input, farm['crop'])
                )

        for crop, data in crop_data.items():
            lower_bound = (data['mean'] - data['stdev'])
            upper_bound = (data['mean'] + data['stdev'])

            for weight in data['dry_weight']:
                if not (lower_bound <= weight <= upper_bound):
                    index = data['dry_weight'].index(weight)
                    output[data['farm_ids'][index]] = crop

        return output if output else None

    def location_check(self):
        '''This method checks whether the GPS coordinates of one farm are
        within 200 meters of another recorded farm'''
        pass

    def duplicate_photo_data(self):
        '''This method checks for duplicate photo submissions'''
        pass

    @staticmethod
    def crop_data_agg(submissions, crop):
        '''This static method generates individual crop data across
        submissions'''

        dry_weights, farm_ids = [], []

        for item in submissions:
            if crop in item.values():
                dry_weights.append(item['dry_weight'])
                farm_ids.append(item['farm_id'])

        return {
            'mean': mean(dry_weights),
            'stdev': stdev(dry_weights),
            'dry_weight': dry_weights,
            'farm_ids': farm_ids
        }
