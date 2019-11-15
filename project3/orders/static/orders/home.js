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
		$('button[id="53_small"]').remove();
		if (window.localStorage.getItem('cart_length')) {
				$("button > span.badge").html(window.localStorage.getItem('cart_length'));
		}
		else {
				$("button > span.badge").html(0);
		}
		$(".list-group-item").click(function() {
				$("#" + $(".list-group-item.active").attr("data-table")).attr("style", "display: none");
				$(".list-group-item.active").removeClass("active");
				$(this).addClass("active");
				$("#" + $(this).attr("data-table")).attr("style", "display: inline");
		});

		$("td button").click(function() {
				$.ajax({
						method: "POST",
						url: $(this).data("url"),
						data: {id: $(this).attr("id"), 
								name: $(this).data("name"),
								type: $('li[data-table = ' + $(this).closest('table').attr("id") + "]").html()
						},
						success: function(data) {
								$("#Modal .modal-dialog").html(data);
						}
				})
		});

		$(".modal-dialog").on('click', '#addToCart', function() {
				var form = $(this).parent().siblings('.modal-body').children('form');
				var formdata = $(form).serialize();
				formdata += "&form_type=" + $(form).attr("id");
				$.ajax({
						method: "POST",
						url: "additem",
						data: formdata,
						success: function(data) {
								if (!(data['success'])) {
										$(form).replaceWith(data['form_html']);
								}
								else {
										$('#Modal').modal('hide');
										let shop_count = $("button > span.badge").html();
										var re = /quantity=(\d*)/;
										var quant = parseInt(re.exec(formdata)[1]);
										window.localStorage.setItem('cart_length', parseInt(shop_count) + quant);
										if (parseInt(shop_count) === 0) {
												window.localStorage.setItem('cart', '[]');
										}
										var cart = JSON.parse(window.localStorage['cart']);
										cart.push(JSON.parse(data['valid_form']));
										window.localStorage.setItem('cart', JSON.stringify(cart));
										$("button  > span.badge").html(parseInt(shop_count) + quant);
										$("#cart_input").attr('value', JSON.stringify(window.localStorage));
										$('#cart_length_input').attr('value', $('button > span.badge').html());
								}
						}
				});
		});
		$('.nav-link#shopping_cart').on('click', function() {
				if (parseInt($("button > span.badge").html()) === 0) {
						$('.navbar').after("<div class='alert alert-warning alert-dismissible fade show' role='alert'>There isn't anything in your shopping cart.<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button></div>");
				}
		});

		$('.list-group-item[data-table="table4"]').click();

});


