#!/usr/bin/python3

from coinbase.wallet.client import Client
from plotext._utility import plot
import yaml
import termcolor
from datetime import datetime
import colorlog
from pathlib import Path
from AccountInfo import AccountInfo
from UserInfo import UserInfo
import plotext as plt

def format_to_red(unformatted_string):
   return termcolor.colored(str(unformatted_string), 'red', attrs=['blink'])

def format_to_green(unformatted_string):
   return termcolor.colored(unformatted_string, 'green', attrs=['blink'])

def format_to_yellow(unformatted_string):
   return termcolor.colored(unformatted_string, 'yellow')

class CoinbaseTrader():
   def __init__(self, verbose = False) -> None:
      self.IsTraderReady = False
      self.api_secret = ""
      self.api_key = ""
      self.trader_wallet_watch_list = list()
      self.watched_accounts = dict()
      self.coinbaseClient = None
      self.verbose = verbose
      self.logger = self.setupLogger()

   def setupLogger(self) -> colorlog:
      # create auxiliary variables
      loggerName = Path(__file__).stem
      # create logger
      logger = colorlog.getLogger(loggerName)
      # create console handler
      consoleHandler = colorlog.StreamHandler()
      consoleHandler.setFormatter(colorlog.ColoredFormatter('%(asctime)s %(log_color)s%(levelname)s:%(name)s %(funcName)20s():%(lineno)s :%(message)s'))
      if self.verbose:
         logger.setLevel(level=colorlog.INFO)
      # Return set up instance
      logger.addHandler(consoleHandler)
      return logger

   def loadConfig(self, config_path) -> bool:
      try:
         credentials=None
         with open(config_path, 'r') as file:
            credentials = yaml.safe_load(file)
            self.api_key=credentials["api-key"]
            self.api_secret=credentials["api-secret"]
            self.trader_wallet_watch_list = credentials["wallet-watch-list"]
            self.logger.info("Loaded Config successfully.")
            return True
      except IOError as ioError:
         self.logger.fatal("Cannot Load config due to IO Error.")
      except Exception as exception:
         self.logger.fatal("Cannot load config.")
      return False

   def check_if_wallet_is_in_watch_list(self, wallet_name) -> bool:
      for watch_list_entity in self.trader_wallet_watch_list:
         if watch_list_entity in wallet_name.lower():
            return True
      return False

   def print_watched_wallets(self) -> None:
      if not self.IsTraderReady:
         self.logger.error("Coinbase Trader client has not been initialized properly.")
         return False
      message = list()
      total = 0
      accounts = self.get_wallet_accounts()
      if len(accounts) != 0:
         message.append('{:25s}|{:>25s}|'.format("Wallet","Amount"))
      else:
         return 
      for wallet_id, wallet in accounts.items():
         if self.check_if_wallet_is_in_watch_list(wallet.wallet_name):
            message.append('{:26s}\t |{:>25s}|'.format(format_to_yellow(wallet.wallet_name),wallet.native_balance.amount))
            value = str(wallet.native_balance.amount).replace('USD','')
            total +=  float(value)
            self.watched_accounts[wallet_id]=wallet
            self.log_multiline_info(wallet)
      message.append('{:25s}|{:>25s}|' .format("Total Balance(USD)",format_to_red("{:25.2f}".format(total))))
      print ('\n'.join( message ))
      return

   def log_multiline_info(self, data_string) -> None:
      self.logger.info("----------------------------------------")
      for line in str(data_string).split("\n"):
         self.logger.info(line)

   def setUpConnection(self, config_path) -> bool:
      if self.loadConfig(config_path):
         try:
            self.coinbaseClient = Client(self.api_key,self.api_secret)
            self.IsTraderReady = True
            self.logger.info("Client connected successfully.")
            return True;
         except Exception as exception:
            self.logger.fatal("Cannot setup Connection to Coinbase servers.")
            return False
      else:
         self.logger.fatal("Failed to load config for connection.")
         return False

   def get_wallet_accounts(self) -> dict():
      if not self.IsTraderReady:
         self.logger.error("Coinbase Trader client has not been initialized properly.")
         return
      accounts = self.coinbaseClient.get_accounts()
      wallet_accounts=dict()
      for wallet_data in accounts["data"]:
         wallet_accounts[wallet_data["id"]]=AccountInfo(wallet_data)
         self.logger.info("Saved ID: {} Type: {} data.".format(wallet_data["id"],wallet_data["name"]))
      return wallet_accounts

   def get_wallet_list_by_currency(self,currency) -> list:
      wallet_by_currency=list()
      wallet_accounts = self.get_wallet_accounts()
      for wallet_id in wallet_accounts:
         if wallet_accounts[wallet_id].currency.upper() == currency.upper():
            wallet_by_currency.append(wallet_accounts[wallet_id])
      return wallet_by_currency


   def get_wallet(self,wallet_id) -> list:
      account_info_json = self.coinbaseClient.get_account(wallet_id)
      if account_info_json is not None:
         account_info=AccountInfo(account_info_json)
         self.log_multiline_info(account_info)
         return account_info
      return None

   def get_current_user(self):
      if not self.IsTraderReady:
         self.logger.error("Coinbase Trader client has not been initialized properly.")
         return None
      user=UserInfo(self.coinbaseClient.get_current_user())
      self.log_multiline_info(user)
      return user

   def get_currency_history(self,wallet_id):
      wallet = self.get_wallet(wallet_id)
      if wallet is not None:
         prices = self.coinbaseClient.get_historic_prices(currency_pair="{}-{}".format(wallet.wallet_balance.currency,wallet.native_balance.currency))
         return prices
      else:
         return None

   def get_wallet_market_trend(self,wallet_id):
      price_list_time_trend=dict()
      price_list=self.get_currency_history(wallet_id)
      if price_list is None:
         return None
      if len(price_list) == 0:
         return None
      for price_point_data in price_list["prices"]:
         time_stamp = datetime.strptime(price_point_data["time"], '%Y-%m-%dT%H:%M:%SZ')
         # price_list_time_trend[time_stamp]=float(price_point_data["price"])
         price_list_time_trend[int(time_stamp.strftime('%s'))]=float(price_point_data["price"])
      return price_list_time_trend

   def plot_pricing_trend(self, wallet_id):
      price_trend = self.get_wallet_market_trend(wallet_id)
      account =  self.get_wallet(wallet_id)
      plt.canvas_color("black")
      plt.axes_color("black")
      plt.ticks_color("yellow")
      plot_date_time=list()
      xticks=[]
      xlabels=[]
      index=1
      for timestamp_epoch in price_trend.keys():
         time_stamp=datetime.fromtimestamp(timestamp_epoch)
         plot_date_time.append(plt.datetime.datetime_to_string(time_stamp))
         if index%20 == 0:
            xticks.append(int(time_stamp.strftime('%s')))
            xlabels.append(plt.datetime.datetime_to_string(time_stamp))
         index+=1
      plt.plot(price_trend.keys(), price_trend.values(), color="green", marker="dot")
      plt.xticks(xticks, xlabels)
      plt.title("Price Trends for {}".format(account.wallet_balance.currency))
      plt.xlabel("Time")
      plt.ylabel("{}".format(account.native_balance.currency))
      plt.show()
