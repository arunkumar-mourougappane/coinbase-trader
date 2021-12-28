#!/usr/bin/python3

from coinbase.wallet.client import Client
import yaml
import termcolor

import colorlog
from pathlib import Path

from AccountInfo import AccountInfo


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
      self.wallet_accounts=dict()
      self.coinbaseClient = None
      self.verbose = verbose
      self.logger = self.setupLogger()

   def setupLogger(self):
      # create auxiliary variables
      loggerName = Path(__file__).stem
      # create logger
      logger = colorlog.getLogger(loggerName)
      # create console handler
      consoleHandler = colorlog.StreamHandler()
      consoleHandler.setFormatter(colorlog.ColoredFormatter('%(asctime)s %(log_color)s%(levelname)s:%(name)s:%(message)s'))
      if self.verbose:
         logger.setLevel(level=colorlog.INFO)
      # Return set up instance
      logger.addHandler(consoleHandler)
      return logger

   def loadConfig(self, config_path):
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

   def check_if_wallet_is_in_watch_list(self, wallet_name):
      for watch_list_entity in self.trader_wallet_watch_list:
         if watch_list_entity in wallet_name.lower():
            return True
      return False

   def print_watched_wallets(self):
      if not self.IsTraderReady:
         self.logger.error("Coinbase Trader client has not been initialized properly.")
         return False
      message = list()
      total = 0
      accounts = self.coinbaseClient.get_accounts()
      for wallet in accounts.data:
         # print(str(wallet))
         if self.check_if_wallet_is_in_watch_list(wallet['name']):
            message.append('{:26s}\t |{:25s}'.format(format_to_yellow(wallet['name']),str(wallet['native_balance'])))
            value = str(wallet['native_balance']).replace('USD','')
            total +=  float(value)
            account=AccountInfo(wallet)
            self.watched_accounts[account.wallet_id]=account
            self.log_account_info(account)
      message.append('{:25s}|{}' .format("Total Balance",format_to_red("USD {:.2f}".format(total))))
      print ('\n'.join( message ))
      return

   def log_account_info(self, account):
      self.logger.info("----------------------------------------")
      for account_data in str(account).split("\n"):
         self.logger.info(account_data)

   def setUpConnection(self, config_path):
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

   def get_wallet_accounts(self):
      if not self.IsTraderReady:
         self.logger.error("Coinbase Trader client has not been initialized properly.")
         return
      accounts = self.coinbaseClient.get_accounts()
      for wallet_data in accounts["data"]:
         self.wallet_accounts[wallet_data["id"]]=AccountInfo(wallet_data)
         self.logger.info("Saved {} data.".format(wallet_data["name"]))

   def list_wallets_by_currency(self,currency):
      wallet_by_currency=list()
      for wallet_id in self.wallet_accounts:
         if self.wallet_accounts[wallet_id].currency == currency.upper():
            wallet_by_currency.append(self.wallet_accounts[wallet_id])
      return wallet_by_currency

def main():
   myTrader = CoinbaseTrader(verbose=True)
   if not myTrader.setUpConnection("credentials.yml"):
      myTrader.logger.error( "Failed to setup connection.")
   else:
      myTrader.logger.info("{}".format( "Coinbase Trader ready for access."))
   if myTrader.IsTraderReady:
      # myTrader.print_watched_wallets()
      myTrader.get_wallet_accounts()
      for wallet in myTrader.list_wallets_by_currency("MATIC"):
         myTrader.log_account_info(wallet)
if __name__ == "__main__":
   main()
