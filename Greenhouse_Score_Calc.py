from math import floor

def score_calc (a,b,c):
    '''
    This function calculates the score of all the combined seeds you have planted at the greenhouse 
    based on the combined seed rank, the combined seed grade, and the cultivation tier.  The score 
    determines your displayed yield, and also the ratio of low quality to high quality items.
    '''
    score = 0
    statboost_coefficient = 0 # This value is important for calculating your chance for obtaining a stat-booster
    quality_ratio = '' #This value determines the ratio of low:high quality items you receive in your yield
    growth_yield = 0 #This is displayed yield
    rank_sum = sum(a)
    a_score = (12 - (rank_sum%12)) * 5
    b_score = floor((float(sum(b))/5)*4)
    c_score = (c + 4)*2
    score = a_score + b_score + c_score
    if 0 < score < 20:
        statboost_coefficient += 1
        quality_ratio += '7:3'
    elif 20 <= score < 40:
        statboost_coefficient += 3
        quality_ratio += '2:8'
    elif 40 <= score < 60:
        statboost_coefficient += 5
        quality_ratio += '7:3'
    elif 60 <= score < 80:
        statboost_coefficient += 10
        quality_ratio += '4:6'
    elif 80 <= score < 90:
        statboost_coefficient += 15
        quality_ratio += '8:2'
    elif 90 <= score <= 100:
        statboost_coefficient += 20
        quality_ratio += '3:7'
    if score <= 40:
        growth_yield += 1
    elif 40 < score <= 80:
        growth_yield += 2
    elif 80 < score <= 100:
        growth_yield += 3

    return score, quality_ratio, statboost_coefficient, growth_yield

def stat_booster_chance (statboost_coefficient, b, c,d): 
    '''
    This function calculates your chance of getting a statbooster from the seeds you plant at the greenhouse.
    This value is calculated separately from your overall quality score, which determines yield.  
    The chance of obtaining a statbooster is determined using the statbooster coefficient, the separate 
    ranks of each seed planted, the cultivation tier, and the type of seed planted
    '''
    stat_booster_dict = {}
    crop_dict = {}
    booster_dict = {'Western Fodlan Seeds' : 'Fruit of Life',
                    'Blue Flower Seeds' : 'Fruit of Life',
                    'Mixed Herb Seeds' : 'Rocky Burdock',
                    'Angelica Seeds' : 'Rocky Burdock',
                    'Purple Flower Seeds' : 'Rocky Burdock',
                    'Southern Fodlan Seeds' : 'Premium Magic Herbs',
                    'Yellow Flower Seeds' : 'Premium Magic Herbs',
                    'Morfis-Plum Seeds' : 'Ailell Pomegranate',
                    'Morfis Seeds' : 'Ailell Pomegranate',
                    'Green Flower Seeds' : 'Ailell Pomegranate',
                    'Nordsalat Seeds' : 'Speed Carrot',
                    'Pale-Blue Flower Seeds' : 'Speed Carrot',
                    'Boa-Fruit Seeds' : 'Miracle Bean',
                    'Mixed-Fruit Seeds' : 'Miracle Bean',
                    'Root Vegetable Seeds' : 'Ambrosia',
                    'Eastern Fodlan Seeds' : 'Ambrosia',
                    'Vegetable Seeds' : 'White Verona',
                    'Red Flower Seeds' : 'White Verona',
                    'Northern Fodlan Seeds' : 'Golden Apple',
                    'Albinean Seeds' : 'Golden Apple',
                    'White Flower Seeds' : 'Golden Apple'}
    #The following dictionary has all the statboosters as keys and the seeds that yield them as values
    for j in d:
        for k in b:
            crop_dict[j] = k
    for key, value in crop_dict.items():
        if key in booster_dict.keys() and booster_dict[key] not in stat_booster_dict:
            stat_booster_dict[booster_dict[key]] = int(statboost_coefficient + ((value-1)*5) + (len(d)*6) + (c*5))
        elif booster_dict[key] in stat_booster_dict:
            continue
    if stat_booster_dict != {}:        
        return stat_booster_dict
    else:
        return ("There is no chance of obtaining a statboosting item with this crop.")

def harvest(c, e, f):
    '''
    This function calculates the total number of items harvested from your crop based on cultivation tier,
    number of seeds planted, and whether or not the Blessings of the Land event is active that day.
    '''
    potential_harvests = {0: ["5-6", "6-7", "7-8",'8-9', '9-10'], 
                          1: [6, 7, 8, 9, 10],
                          2: [7, 8, 9, 10, 11],
                          3: [8, 9, 10, 11, 12],
                          4: [9, 10, 11, 12, 13],
                          5: [10, 11, 12, 13, 14],
                          6: [11, 12, 13, 14, 15]}   
    harvest = 0
    potential_harvest = potential_harvests[c]
    harvest = potential_harvest[e-1]
    if f == "Yes":
        if type(harvest) is int:
            harvest += 5
        else:
            harvest_list = list(map(int, harvest.split('-')))
            for h in harvest_list:
                h +=5
            harvest = harvest_list.join('-')

    return harvest




    


if __name__ == '__main__':
    a = input("Enter ranks of seeds planted: ")
    '''Each seed has a hidden rank value.  Find the rank values online 
    and enter them spaced out, with no commas.'''
    a = list(map(str, a.split(' ')))
    a = [int(rank) for rank in a]
    b = input("Enter grades of seeds planted: ")
    ''' The grade for each seed is the 1-5 star rating that is displayed when you select it in-game. 
    Enter these again with a space between each value and with no commas or other punctuation. '''
    b = list(map(str, b.split(' ')))
    b = [int(grade) for grade in b]
    c = int(input("Enter cultivation tier: "))
    #The cultivation tier goes from 1 for infusing with magic to 6 for applying pegasus blessings
    d = input("Enter the names of seeds planted: ")
    #This is necessary for calculating the chance of getting a stat-boosting item. Enter items with a comma and a space to separate
    d = list(map(str, d.split(', ')))
    e = int(input("Enter the number of seeds you are planting: "))
    f = input("Is the Blessings of the Land event active?: ")
    score, quality_ratio, statboost_coefficient, growth_yield =score_calc(a,b,c)
    print("This yield has a score of {}, a quality ratio of {}, and a yield of {}.".format(score, quality_ratio, growth_yield))
    booster_chances = stat_booster_chance(statboost_coefficient, b, c, d)
    booster_chance = list(booster_chances.values())[0]
    boosters = list(booster_chances.keys())
    crop_yield = harvest(c,e,f)
    #print(booster_chances)
    print('''There is a {} chance of obtaining one of {} following statboosters:
    {}.'''.format(booster_chance, len(boosters), boosters))
    if booster_chances != {}:
        print("This crop will yield a harvest of {} items along with 1 statbooster.".format(crop_yield))
    else:
        print('This crop will yield a harvest of {} items and no statboosters.'. format(crop_yield))
