#! /usr/bin/python3

from Country import Country
from datetime import datetime


class Nationality:
   def __init__(self, nationality_code, nationality_name):
      self.nationality_code = nationality_code
      self.nationality_name = nationality_name


class UserInfo():
   def __init__(self, user_json):
      self.avatar_url = user_json["avatar_url"]
      self.name = user_json["name"]
      self.country = Country(user_json["country"]["code"], user_json["country"]["name"], user_json["country"]["is_in_europe"])
      self.email = user_json["email"]
      self.has_blocking_buy_restrictions = user_json["has_blocking_buy_restrictions"]
      self.has_buy_deposit_payment_methods = user_json["has_buy_deposit_payment_methods"]
      self.has_made_a_purchase = user_json["has_made_a_purchase"]
      self.has_unverified_buy_deposit_payment_methods = user_json["has_unverified_buy_deposit_payment_methods"]
      self.user_id = user_json["id"]
      self.legacy_user_id = user_json["legacy_id"]
      self.native_currency = user_json["native_currency"]
      self.nationality = Nationality(user_json["nationality"]["code"], user_json["nationality"]["name"])
      self.state = user_json["state"]
      self.time_zone = user_json["time_zone"]
      self.username = user_json["username"]
      self.created_at = datetime.strptime(user_json["created_at"], '%Y-%m-%dT%H:%M:%SZ')

   def __repr__(self):
      user_data = list()
      user_data.append("Name: {}".format(self.name))
      user_data.append("Username: {}".format(self.username))
      user_data.append("Id: {}".format(self.user_id))
      user_data.append("{}".format(self.email))
      user_data.append("Native Currency: {}".format(self.native_currency))
      user_data.append("Nationality: {}".format(self.nationality.nationality_name))
      user_data.append("Country of Residence: {}".format(self.country.country_name))
      user_data.append("State: {}".format(self.state))
      return "\n".join(user_data)
