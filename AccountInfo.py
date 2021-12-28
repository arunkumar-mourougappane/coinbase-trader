#! /usr/bin/python3

class Balance():
   def __init__(self, amount, currency):
      self.amount=amount
      self.currency=currency
   def __repr__(self):
      return "Amount: {} {}".format(self.amount, self.currency)

class AccountInfo():
   def __init__(self, wallet_data):
      self.wallet_id=wallet_data["id"]
      self.currency=wallet_data["currency"]
      self.wallet_name=wallet_data["name"]
      self.wallet_balance=Balance(wallet_data["balance"]["amount"],wallet_data["balance"]["currency"])
      self.native_balance=Balance(wallet_data["native_balance"]["amount"],wallet_data["native_balance"]["currency"])
      self.allow_deposits=wallet_data["allow_deposits"]
      self.allow_withdrawls=wallet_data["allow_withdrawals"]
   def __repr__(self):
      wallet_data=list()
      wallet_data.append("Wallet Name: {}".format(self.wallet_name))
      wallet_data.append("Wallet ID: {}".format(self.wallet_id))
      wallet_data.append("Wallet Currency: {}".format(self.currency))
      wallet_data.append("Balance:")
      wallet_data.append("\t{}".format(self.wallet_balance))
      wallet_data.append("Native Balance:")
      wallet_data.append("\t{}".format(self.native_balance))
      wallet_data.append("Allow Withdrawls: {}".format("Yes" if self.allow_withdrawls else "No"))
      wallet_data.append("Allowe Deposits: {}".format("Yes" if self.allow_deposits else "No"))
      return '\n'.join( wallet_data )
