'''The harvest data validator module'''

from statistics import stdev, mean
from geopy.distance import distance
from itertools import combinations
from PIL import Image
from imagehash import average_hash
from os.path import join


class DataValidator:
    '''This class indentifies issues in a provided json data set'''

    def __init__(self, crop_data, image_data, images_dir):
        self.input = crop_data['harvest_measurements']
        self.image_files = image_data
        self.image_dir = images_dir

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
                if not (lower_bound < weight < upper_bound):
                    index = data['dry_weight'].index(weight)
                    output[data['farm_ids'][index]] = crop

        return output if output else None

    def location_check(self):
        '''This method checks whether the GPS coordinates of one farm are
        within 200 meters of another recorded farm'''

        output, locs = {}, []

        # prepare a list of locations tuples
        for farm in self.input:
            locs.append(tuple([float(x.strip()) for x in farm[
                'location'].split(',')]))

        # validate the distances between unique locations
        for loc1, loc2 in combinations(locs, 2):
            if loc1 != loc2:
                if distance(loc1, loc2).meters <= 200:
                    res = DataValidator.loc_farm_match(self.input, loc1, loc2)
                    output[res[0]] = res[1]

        return output if output else None

    def duplicate_photo_data(self):
        '''This method checks for duplicate photo submissions'''

        resize_matrix, img_hashes, output = 10, {}, {}

        for img_name in self.image_files:
            with Image.open(join(self.image_dir, img_name)) as img:
                curr_hash = average_hash(img, resize_matrix)

                if curr_hash not in img_hashes:
                    img_hashes[curr_hash] = img_name
                else:
                    output[img_hashes[curr_hash]] = img_name

        return output if output else None

    @staticmethod
    def crop_data_agg(submissions, crop):
        '''This method generates individual crop data across all
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

    @staticmethod
    def loc_farm_match(submissions, loc1, loc2):
        '''This method matches farm coordinates to farm id'''

        loc1_id, loc2_id = '', ''

        for farm in submissions:
            curr_loc = tuple([float(x.strip()) for x in farm[
                'location'].split(',')])

            if curr_loc == loc1:
                loc1_id = farm['farm_id']

            elif curr_loc == loc2:
                loc2_id = farm['farm_id']

        return (loc1_id, loc2_id)
