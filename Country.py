#!/usr/bin/python3

class Country():
   def __init__(self, country_code, country_name, is_in_europe=False):
      self.country_code = country_code
      self.country_name = country_name
      self.is_in_europe = is_in_europe