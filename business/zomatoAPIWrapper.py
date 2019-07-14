from os.path import join
from business import utils
from configs.config import get_config

credential = get_config("configs/credentials.yaml")


class ZomatoAPIWrapper:    
    
    def __init__(self,
                url="https://developers.zomato.com/api/", 
                version="v2.1", 
                api_key=credential["ZOMATO_API_KEY"],
                file_format="json"):
                
        self.url = join(url, version)
        self.user_key = api_key
        self.file_format = file_format
        
    def __repr__(self):
        
        return self.url
        
    def headers(self):
        
        headers = {
            "user-key": self.user_key,
            "Accept": self.file_format
            }
        
        return headers
    
    def query(self, search_key, **kwargs):
        """
        Helper function to return String url of query against Zomato
        """
    
        url = join(self.url, search_key)
        
        if kwargs is not None:
            argument = ""
            for key, value in kwargs.items():
                if value is not None:
                    argument += "&{}={}".format(key, value)
        
        # Do not forget to remove first "&"
        return url + argument[1:]
    
    def get_location_information(self, query, 
                                 search_key="locations?",
                                 lat=None, lon=None, count=10):
        
        kwargs = {"query": query,
                 "lat": lat,
                 "lon": lon,
                 "count": count}
        
        full_url = self.query(search_key, **kwargs)
        api_call = utils.load_and_convert_json(full_url, self.headers(), "location_suggestions")
    
        return api_call
    
    def get_location_details(self, 
                            search_key="location_details?",
                            entity_id=None, entity_type=None):
                            
        kwargs = {"entity_id": entity_id,
                "entity_type": entity_type}
                
        full_url = self.query(search_key, **kwargs)
        api_call = utils.load_and_convert_json(full_url, self.headers())
    
        return api_call
    
    def get_list_of_cuisines_in_city(self, city_id,
                                    search_key="cuisines?",
                                    target_in_json="cuisines",
                                    lat=None, lon=None):
        
        """
        Return a list of cuisine_id of all cuisine type in a city_id
        """
        
        kwargs = {"city_id": city_id,
                 "lat": lat,
                 "lon": lon}
        
        full_url = self.query(search_key, **kwargs)
        api_call = utils.load_and_convert_json(full_url, self.headers(), target_in_json)
        
        return api_call
    
    def search_for_restaurants(self, 
                              search_key="search?",
                              target_in_json="restaurants",
                              entity_id=None, entity_type=None, query=None,
                              start=0, count=20, lat=None, lon=None, radius=None,
                              cuisines=None, establishment_type=None, collection_id=None,
                              category=None, sort="cost", order="asc"):
        
        kwargs = {"entity_id": entity_id,
                 "entity_type": entity_type,
                 "query": query,
                 "start": start,
                 "count": count,
                 "lat": lat,
                 "lon": lon,
                 "radius": radius,
                 "cuisines": cuisines,
                 "establishment_type": establishment_type,
                 "collection_id": collection_id,
                 "category": category,
                 "sort": sort,
                 "order": order}
        
        full_url = self.query(search_key, **kwargs)
        api_call = utils.load_and_convert_json(full_url, self.headers(), target_in_json)
        
        return api_call