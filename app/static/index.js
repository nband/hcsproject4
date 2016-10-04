$(function(){ 
	var selectingToAccount = false;
	var selectingFromAccount = false;

	var idOfSelectedToAccount;
	var idOfSelectedFromAccount;


	/* ========== Selecting To Account Button ========== */

	$("#selectTransferToBtn").click(function() {
		$(".account").filter(function() {
				return !(isSelected($(this)));
			}).css(selectingAccountsCss);

		selectingToAccount = true;
		selectingFromAccount = false;
	});


	/* ========== Selecting From Account Button ========== */

	$("#selectTransferFromBtn").click(function() {
		$(".account").filter(function() {
				return !(isSelected($(this)));
			}).css(selectingAccountsCss);
		
		selectingFromAccount = true;
		selectingToAccount = false;
	});


	/* ========== Account Selection ========== */

	var resetSelections = {
		'selectedToAccount': false,
		'selectedFromAccount': false
	};

	// set all accounts as not selected
	$(".account").data(resetSelections);
	
	$(".account").click(function() {
		var isToAccountSelected = $(this).data('selectedToAccount');
		var isFromAccountSelected = $(this).data('selectedFromAccount')
		var selected = isToAccountSelected || isFromAccountSelected;
		
		if (selectingToAccount) {
			// mark this account as selected
			$(this).data('selectedToAccount', true);
			$(this).data('selectedFromAccount', false);

			// store the id of this account
			idOfSelectedToAccount = $(this).attr('id')

			// update the UI to show which account was selected
			$("#transferToAccount").text($(this).find(".nickname").text());

			// reset all borders on accounts
			$(".account").filter(function() {
				return !(isFromSelected($(this)));
			}).css(emptyBorder);

			// clear any other To Account selections that have been made
			resetToData();

			// add a border to the selected account to show it's selected
			$('#' + idOfSelectedToAccount).css(selectedToAccountCss);

			selectingToAccount = false;
		} else if (selectingFromAccount) {
			// mark this account as selected
			$(this).data('selectedFromAccount', true);
			$(this).data('selectedToAccount', false);

			// store the id of this account
			idOfSelectedFromAccount = $(this).attr('id')

			// update the UI to show which account was selected
			$("#transferFromAccount").text($(this).find(".nickname").text());

			// reset all borders on accounts
			$(".account").filter(function() {
				return !(isToSelected($(this)))
			}).css(emptyBorder);

			// clear any other From Account selections that have been made
			resetFromData();

			// add a border to the selected account to show it's selected
			$('#' + idOfSelectedFromAccount).css(selectedFromAccountCss);

			selectingFromAccount = false;
		} else if (selected) {
			if (isToAccountSelected) {
				$("#transferToAccount").text("");
			} else if (isFromAccountSelected) {
				$("#transferFromAccount").text("");
			}

			$(this).data(resetSelections)
			$(this).css(emptyBorder);
		}
	});



	/* ========== Helper Methods ========== */

	var isSelected = function(obj) {
		return obj.data('selectedToAccount') == true;
	}

	var isToSelected = function(obj) {
		return obj.data('selectedToAccount') == true;
	}

	var isFromSelected = function(obj) {
		return obj.data('selectedFromAccount') == true;
	}

	var resetToData = function() {
		$(".account").filter(function() {
			return $(this).data("selectedToAccount") == true
		}).data("selectedToAccount", false);
	}

	var resetFromData = function() {
		$(".account").filter(function() {
			return $(this).data("selectedFromAccount") == true
		}).data("selectedFromAccount", false);
	}


	/* ========== CSS Helper Library ========== */

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

});