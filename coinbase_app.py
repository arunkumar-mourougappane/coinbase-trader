#!/usr/bin/python3

from CoinbaseTrader import CoinbaseTrader


def main():
   myTrader = CoinbaseTrader(verbose=False)
   if not myTrader.setUpConnection("credentials.yml"):
      myTrader.logger.error("Failed to setup connection.")
   else:
      myTrader.logger.info("{}".format("Coinbase Trader ready for access."))
   if myTrader.IsTraderReady:
      print("*************** Wallet Account By Currency ***************")
      for wallet in myTrader.get_wallet_list_by_currency("DOGE"):
         print(wallet)
      print("*************** User Information ***************")
      print(myTrader.get_current_user())
      print("*************** Watched Accounts ***************")
      myTrader.print_watched_wallets()
      our_accounts = myTrader.get_watched_wallet_accounts()
      print("*************** Watched Accounts Data ***************")
      for account_id in our_accounts:
         print(our_accounts[account_id])
      new_list = list(our_accounts.keys())
      myTrader.plot_live_trends_for_list(new_list)


if __name__ == "__main__":
   main()
