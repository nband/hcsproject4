$(function(){ 
	var selectingToAccount = false;
	var selectingFromAccount = false;

	var idOfSelectedToAccount;
	var idOfSelectedFromAccount;

	var selectingAccountsCss = {
		'border-style': 'solid',
		'border-color': '#b94a48',
		'border-width': '5px'
	}

	var selectedToAccountCss = {
		'border-style': 'solid',
		'border-color': 'green',
		'border-width': '5px'
	}

	var selectedFromAccountCss = {
		'border-style': 'solid',
		'border-color': 'black',
		'border-width': '5px'
	}

	var emptyBorder = {
		'border-style': '',
		'border-color': '',
		'border-width': ''	
	}

	$("#selectTransferToBtn").click(function() {
		$(".account").css(selectingAccountsCss);
		selectingToAccount = true;
		selectingFromAccount = false;
	});

	$("#selectTransferFromBtn").click(function() {
		$(".account").css(selectingAccountsCss);
		selectingFromAccount = true;
		selectingToAccount = false;
	});

	$(".account").click(function() {
		if (selectingToAccount) {
			// store the id of this account
			idOfSelectedToAccount = $(this).attr('id')

			// update the UI to show which account was selected
			$("#transferToAccount").text($(this).find(".nickname").text());

			// reset all borders on accounts
			$(".account").css(emptyBorder);

			// add a border to the selected account to show it's selected
			$('#' + idOfSelectedToAccount).css(selectedToAccountCss);
		} else if (selectingFromAccount) {
			// store the id of this account
			idOfSelectedFromAccount = $(this).attr('id')

			// update the UI to show which account was selected
			$("#transferFromAccount").text($(this).find(".nickname").text());

			// reset all borders on accounts
			$(".account").css(emptyBorder);

			// add a border to the selected account to show it's selected
			$('#' + idOfSelectedFromAccount).css(selectedFromAccountCss);
		}
	});

});