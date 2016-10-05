from flask import render_template, request
from app import app

import requests
import json
import datetime

from app.utils import format_price

from enum import Enum

apiKey = "8c9f951688f6cf33204c1711017c5660";

class Medium(Enum):
	BALANCE = "balance"
	REWARDS = "rewards"

# http://www.davidadamojr.com/handling-cors-requests-in-flask-restful-apis/
@app.after_request
def after_request(response):
	print response
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
	
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)

		# filter out credit card accounts (can't transfer money to/from them)
		accountsNoCards = []
		for account in accounts:
			if account["type"] != "Credit Card":
				accountsNoCards.append(account);

		transfers = []
		# for each account make a request to get it's transfers where it is the payer only...
		for account in accountsNoCards:
			transfersUrl = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(account['_id'], apiKey)
			transfersResponse = requests.get(transfersUrl)

			if transfersResponse.status_code == 200:
				transfers.extend(json.loads(transfersResponse.text))

		return render_template("home.html", accounts=accountsNoCards, format_price=format_price, transfers=transfers)
	else:
		return render_template("notfound.html")

# Transfer post route.  Makes request to Nessie API to create a transfer.
@app.route('/transfer', methods=['POST'])
def postTransfer():
	# get values from the request (populated by user into the form)
	toAccount = request.form["toAccount"]
	fromAccount = request.form["fromAccount"]
	amount = float(request.form["amount"]) # need to convert to an int or this fails
	description = request.form["description"]
	
	medium = Medium.BALANCE;
	dateObject = datetime.date.today()
	dateString = dateObject.strftime('%Y-%m-%d')

	body = {
		'medium' : medium,
		'payee_id' : toAccount,
		'amount' : amount,
		'transaction_date' : dateString,
		'description' : description
	}
	print(body)

	url = "http://api.reimaginebanking.com/accounts/{}/transfers?key={}".format(fromAccount, apiKey)
	response = requests.post(
		url,
		data=json.dumps(body),
		headers={'content-type':'application/json'},)

	print(response.text)
	return render_template("notfound.html")
