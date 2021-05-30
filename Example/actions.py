
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
import requests
import json


class ActionGetCountryList(Action):

    def name(self):
        return "action_check_for_country"

    def run(self, dispatcher, tracker, domain):
      
        response = requests.get("https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries")
        country_data = response.json()
        countries = country_data['body']

        return [SlotSet('countries',countries)]

class CapitalCheckForm(FormValidationAction):
    def name(self):
        return "validate_check_for_capital_form"

    @staticmethod
    async def required_slots(self,slots_mapped_in_domain, dispatcher , tracker):
        print("Inside required slot")
        return ['country']

    def validate_country(self, value, dispatcher, tracker, domain):
        print('validate value of country ', value)

        try:
            response = requests.get("https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries")
            country_data = response.json()
            countries = country_data['body']
            print('countries',countries)
            cntry = [country for country in countries if country.upper() == value.upper()]
            print(cntry[0],"cntry")
            return{"country": cntry[0]}

        except:
            dispatcher.utter_template("utter_wrong_country",tracker)
            return{"country": None}
        
class PopulationCheckForm(FormValidationAction):

   
    def name(self):
        return "validate_check_for_population_form"

    @staticmethod
    async def required_slots(self,slots_mapped_in_domain, dispatcher , tracker):
        print("Inside required slot")
        return ["country"]

    
    def validate_country(self, value, dispatcher, tracker,domain):
        print('validate value of country ', value)
        
        try:
            response = requests.get("https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries")
            country_data = response.json()
            countries = country_data['body']
            print('countries',countries)
            cntry = [country for country in countries if country.upper() == value.upper()]
            print(cntry,"cntry")
            if cntry:
                print("inside if")
                
                return {"country": cntry[0]}
            else:
                dispatcher.utter_template("utter_wrong_country",tracker)
                return {"country": None}
        except:
            dispatcher.utter_template("utter_wrong_country",tracker)
            return {"country": None}


class ActionCapital(Action):   #action to capture capital of provide country
    
    def name(self):
        return "action_capital"

    
    def run(self, dispatcher, tracker, domain):  
        print("reset")

        url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCapital"
        data_capital = json.dumps({"country": "{}".format(tracker.get_slot('country')),"Content-Type": "application/json"})
        print(data_capital)
        response = requests.post(url=url,data = data_capital)
        print("post api response",response.status_code)
        capital_data = response.json()
        print(capital_data['success'])
        if capital_data['success'] == 1:
            capital = capital_data['body']['capital'] 
            country = capital_data['body']['country']
            dispatcher.utter_message("{} is capital of {}".format(capital,country))
        elif capital_data['success'] == 0:
             dispatcher.utter_message("{} is capital of not available".format(capital))
        return [SlotSet('country',None)]

class ActionPopulation(Action):  #action to check population of provide country

    def name(self):
        return "action_population"
    
    
    def run(self, dispatcher, tracker, domain):
        print("reset")

        url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation"
        data_population = json.dumps({"country": "{}".format(tracker.get_slot('country')),"Content-Type": "application/json"})
        print(data_population)
        response = requests.post(url=url,data = data_population)
        print("post api response",response.status_code)
        population_data = response.json()
        print(population_data['success'])
        if population_data['success'] == 1:
            population = population_data['body']['population'] 
            country = population_data['body']['country']
            dispatcher.utter_message("Population of {} is {}".format(country,population))
        elif population_data['success'] == 0:
            dispatcher.utter_message("Population of {} is not available".format(country))
    
        return [SlotSet('country',None)]

