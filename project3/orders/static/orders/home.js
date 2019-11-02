$(document).ready(function() {
		$(".list-group-item").click(function() {
				$("#" + $(".list-group-item.active").attr("data-table")).attr("style", "display: none");
				$(".list-group-item.active").removeClass("active");
				$(this).addClass("active");
				$("#" + $(this).attr("data-table")).attr("style", "display: inline");
		});

		$("td button").click(function() {
				let shop_count = $("a > span.badge").html();
				$("a > span.badge").html(parseInt(shop_count) + 1);
				//1,2,3 topping pizzas
				if (['3', '5', '7'].includes($(this).attr('id')[0])) {
						$.ajax({
								method: "GET",
								url: $(this).data("url"),
								data: {toppings: $(this).data("toppings")[0]}
								success: function(data) {
									$("#PizzaModal .modal-body").html(data);
								}
						})
				}
		});
});
