from flask import render_template, request, redirect
from app import app

import requests
import json
import datetime

from app.utils import format_price

from enum import Enum

# move this to a config file that will not be included in the repo
apiKey = "8c9f951688f6cf33204c1711017c5660";

# enum for the medium of transfer
#  * balance - currency
#  * rewards - rewards points
class Medium(Enum):
	BALANCE = "balance"
	REWARDS = "rewards"

# http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
	return response

# Home page route. Loads the accounts.
@app.route('/')
@app.route('/index')
def index():
	# create the URL for the request
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)

	# make call to the Nessie Accounts endpoint
	accountsResponse = requests.get(accountsUrl)
	
	# if the accounts call responds with success
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)

		# filter out credit card accounts (can't transfer money to/from them)
		accountsNoCards = []
		for account in accounts:
			if account["type"] != "Credit Card":
				accountsNoCards.append(account);

		# variable which will keep track of all transfers to pass to UI
		transfers = []
		
		# for each account make a request to get it's transfers where it is the payer only...
		for account in accountsNoCards:
			transfersUrl = 'http://api.reimaginebanking.com/accounts/{}/transfers?type=payer&key={}'.format(account['_id'], apiKey)
			transfersResponse = requests.get(transfersUrl)

			# if the transfer GET request was successful, add the resulting transfers to the array of data
			if transfersResponse.status_code == 200:
				transfers.extend(json.loads(transfersResponse.text))

		return render_template("home.html", accounts=accountsNoCards, format_price=format_price, transfers=transfers)
	else:
		return render_template("notfound.html")

# Transfer post route.  Makes request to Nessie API to create a transfer.
@app.route('/transfer', methods=['POST'])
def postTransfer():
	print("MADE IT HERE")
	# get values from the request (populated by user into the form on the UI)
	toAccount = request.form["toAccount"]
	fromAccount = request.form["fromAccount"]
	amount = float(request.form["amount"]) # need to convert to an int or this fails
	description = request.form["description"]
	
	# set values that are not included in the form
	medium = Medium.BALANCE;
	dateObject = datetime.date.today()
	dateString = dateObject.strftime('%Y-%m-%d')

	# set up payload for request
	body = {
		'medium' : medium,
		'payee_id' : toAccount,
		'amount' : amount,
		'transaction_date' : dateString,
		'description' : description
	}

	# make the request to create the transfer
	url = "http://api.reimaginebanking.com/accounts/{}/transfers?key={}".format(fromAccount, apiKey)
	response = requests.post(
		url,
		data=json.dumps(body),
		headers={'content-type':'application/json'},)

	# redirect user to the same page, which should now show there latest transaction in the list
	return redirect("/index", code=302)
