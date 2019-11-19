function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
				var cookies = document.cookie.split(';');
				for (var i = 0; i < cookies.length; i++) {
						var cookie = cookies[i].trim();
						// Does this cookie string begin with the name we want?
						if (cookie.substring(0, name.length + 1) === (name + '=')) {
								cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
								break;
						}
				}
		}
		return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
		beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
		}
});


$(document).ready(function() {
		$(".btn.btn-light").on('click', function() {
				$.ajax({
						url: 'delete',
						method: "POST",
						data: {'id': $(this).attr('id')},
						success: function(data) {
								if (!data['success']) {
										throw "Something went wrong deleting";
								}
								else {
										let price = parseFloat($("#" + data['item_id']).parent().siblings('.item-price').html().slice(1));
										$("#" + data['item_id']).parent().parent().fadeOut('slow', function() { $(this).remove(); });
										let total = parseFloat($('#total').html().match(/\$(.*)/)[1]);
										$('#total').html('Total: $' + (total - price).toFixed(2).toString());
										if (parseFloat($('#total').html().match(/\$(.*)/)[1]) === 0) {
												$('#returnToShopping')[0].click();
										};
								}
						}
				});
		});
		$("#place_order").on('click', function() {
				$.ajax({
						url: 'place_order',
						method: "POST",
						success: function(data) {
								if (!data['success']) {
										throw "Something went wrong completing your order";
								}
								else {
										alert("Your order has been placed and will be ready for pickup soon. Thanks for shopping.");
										$('#returnToShopping')[0].click();
								};
						}
		});
});
});
