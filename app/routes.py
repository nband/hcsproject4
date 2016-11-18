from flask import render_template, request, redirect
from app import app

import requests
import json
import datetime

from app.utils import format_price

from enum import Enum

# move this to a config file that will not be included in the repo
apiKey = app.config["API_KEY"] # get the API Key from the config file

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

		# filter out any credit card accounts (can't transfer money to/from them)
		accountsNoCards = []
		for account in accounts:
			if account["type"] != "Credit Card":
				accountsNoCards.append(account);

		# variable which will keep track of all transfers to pass to UI
		transfers = []
		
		# for each account make a request to get it's transfers where it is the payer only...
		for account in accounts:
			transfersUrl = 'http://api.reimaginebanking.com/accounts/{}/transfers?type=payer&key={}'.format(account['_id'], apiKey)
			transfersResponse = requests.get(transfersUrl)

			# if the transfer GET request was successful, add the resulting transfers to the array of data
			if transfersResponse.status_code == 200:
				transfers.extend(json.loads(transfersResponse.text))

		return render_template("home.html", accounts=accounts, format_price=format_price, transfers=transfers)
	else:
		return render_template("notfound.html")

# Transfer post route.  Makes request to Nessie API to create a transfer.
@app.route('/transfer', methods=['POST'])
def postTransfer():
	# get values from the request (populated by user into the form on the UI)
	# (added some error handling here for invalid form input)
	fromAccount = request.form["fromAccount"]
	if fromAccount == "":
		return redirect("/index", code=302)
	
	toAccount = request.form["toAccount"]
	try:
		amount = float(request.form["amount"]) # need to convert to an int or this fails
	except ValueError:
		amount = ""
	
	description = request.form["description"]
	
	# set values that are not included in the form
	medium = "balance";
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

# Post route for conducting purchases. 
@app.route('/purchase', methods=['POST'])
def purchase():
	
	
	# get the fixed account value from the HTML form
	# NOTE - I encountered issues in getting ACCOUNT ID's specifically
	# so, this step actually just gets "insertidhere" in the field
	Account = request.form["Account"]
	if Account == "":
		return redirect("/index", code=302)
	
	Merchant = request.form["Merchant"]
	try:
		amount = float(request.form["amount"]) # need to convert to an int or this fails
	except ValueError:
		amount = ""
	
	description = request.form["description"]
	
	# set values that are not included in the form
	medium = "balance";
	dateObject = datetime.date.today()
	dateString = dateObject.strftime('%Y-%m-%d')

	# set up payload for request
	body = {
		'medium' : medium,
		'payee_id' : Merchant,
		'amount' : amount,
		'transaction_date' : dateString,
		'description' : description
	}

	# make the request to create the transfer
	url = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(Account, apiKey)
	response = requests.post(
		url,
		data=json.dumps(body),
		headers={'content-type':'application/json'},)

	# redirect user to the index page
	return redirect("/index", code=302)
	
# Load the purchases. 
@app.route('/purchaseList', methods=['GET'])
def purchaseList():
	
	# create the URL for the request
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)

	# make call to the Nessie Accounts endpoint
	accountsResponse = requests.get(accountsUrl)
	
	# if the accounts call responds with success
	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
	
	# create the URL for the request
	purchasesUrl = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(accounts['_id'], apiKey)

	# make call to the Nessie Accounts endpoint
	purchasesResponse = requests.get(purchasesUrl)
	
	# if the accounts call responds with success
	if purchasesResponse.status_code == 200:
		purchases = json.loads(purchasesResponse.text)

		# variable which will keep track of all purchases to pass to UI
		purchases = []
		
		# for each account make a request to get it's transfers where it is the payer only...
		for account in accounts:
			purchasesURL = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(accounts['_id'], apiKey)
			purchasesResponse = requests.get(purchasesUrl)

			# if the transfer GET request was successful, add the resulting transfers to the array of data
			if purchasesResponse.status_code == 200:
				purchases.extend(json.loads(purchasesResponse.text))

		return render_template("purchaseList.html", accounts=accounts, format_price=format_price, purchases=purchases)