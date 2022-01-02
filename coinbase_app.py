#!/usr/bin/python3

from CoinbaseTrader import CoinbaseTrader
import argparse
import plotext as plt

def main():
   parser = argparse.ArgumentParser()
   
   myTrader = CoinbaseTrader(verbose=False)
   if not myTrader.setUpConnection("credentials.yml"):
      myTrader.logger.error( "Failed to setup connection.")
   else:
      myTrader.logger.info("{}".format( "Coinbase Trader ready for access."))
   if myTrader.IsTraderReady:
      print("*************** Watched Accounts ***************")
      myTrader.print_watched_wallets()
      print("*************** Wallet Account By Currency ***************")
      for wallet in myTrader.get_wallet_list_by_currency("BTC"):
         print(wallet)
      print("*************** User Information ***************")
      print(myTrader.get_current_user())
      print("*************** Account Trend ***************")
      price_trend=myTrader.plot_pricing_trend("c008f295-6a38-558b-8c8c-168d5b1d9c2d")

if __name__ == "__main__":
   main()
