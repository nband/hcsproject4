from flask import render_template
from app import app

import requests
import json
import json

from app.utils import format_price

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
	apiKey = "8c9f951688f6cf33204c1711017c5660";
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

		return render_template("home.html", accounts=accountsNoCards, format_price=format_price)
	else:
		return render_template("notfound.html")

# Transfer post route.  Makes request to Nessie API to create a transfer.
@app.route('/transfer', methods=['POST'])
def postTransfer():
	# get data here and do something with it...
	return render_template("notfound.html")
