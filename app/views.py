from flask import render_template
from app import app

import requests
import json
import json

@app.route('/')
@app.route('/index')
def index():

	# create the URL for the request
	apiKey = "8c9f951688f6cf33204c1711017c5660";
	accountsUrl = 'http://api.reimaginebanking.com/accounts?key={}'.format(apiKey)

	customersUrl = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)

	# make call to the Nessie Accounts endpoint
	accountsResponse = requests.get(accountsUrl)

	customersResponse = requests.get(customersUrl)

	if accountsResponse.status_code == 200:
		accounts = json.loads(accountsResponse.text)
		customers = json.loads(customersResponse.text)
		return render_template("home.html", accounts=accounts, customers=customersResponse)
	else:
		return render_template("notfound.html")