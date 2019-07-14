import requests # To do HTTP requests
import json # To parse JSON files

from numpy.random import choice

from business.zomatoAPIWrapper import ZomatoAPIWrapper


def load_and_convert_json(url, headers, query=None):
    """
    Load data from String url and
    return the Python dictionary version of data
    """

    request = requests.get(url, headers=headers)
    
    if request.status_code == requests.codes.ok:
        api_call = json.loads(request.text)
        
        if query is not None:
            return api_call[query]
        
        return api_call
        
    raise Exception("Request status code is {}".format(request.status_code))


def apply_conversion_logic(entity):
    """
    Helper function to smartly convert entity into dictionary, if not already is.
    """
    if type(entity) is str:
        return json.loads(entity)
    elif type(entity) is dict:
        return entity
    else:
        raise Exception("location_entity is {}".format(type(entity)))    


def filter_location(query):
    
    api = ZomatoAPIWrapper()
    locations = api.get_location_information(query)
    
    return locations        

def check_restaurant_cuisines(cuisines_list):
    CUISINE_FORBIDDENS = [
        "Cafe",
        "Bakery", 
        "Beverages",
        "Bubble Tea",
        "Coffee",
        "Coffee and Tea",
        "Desserts",
        "Drinks Only",
        "Ice Cream",
        "Juices",
        "Patisserie",
        "Tea",
    ]
    
    # Need update
    LOCALITY_FORBIDDENS = [
        "Thai",
        "Chinese",
        "Japanese",
        "Indonesian",
        "Korean", 
        "Western",
        "Taiwanese"
    ]
    
    tmp = []
    
    for cuisine in cuisines_list:
        if cuisine not in LOCALITY_FORBIDDENS + CUISINE_FORBIDDENS:
            tmp.append(False)
    
    return all(tmp)
    
def generate_restaurant(loc_id, loc_type, restaurant_count):
    
    zomato = ZomatoAPIWrapper()
    is_forbidden = True
    
    while is_forbidden:
        # p is there to later modify probability of getting a certain number
        random_num = choice(restaurant_count, 1, p=[1/restaurant_count for i in range(restaurant_count)])[0]

        random_restaurant = zomato.search_for_restaurants(entity_id=loc_id, entity_type=loc_type,
                                                     start=random_num, count=1)
        
        print(random_num, restaurant_count)
        try:
            cuisines = random_restaurant[0]["restaurant"]["cuisines"].split(", ")
            is_forbidden = check_restaurant_cuisines(cuisines)
            
        except:
            is_forbidden = True
        
    return random_restaurant[0]["restaurant"]