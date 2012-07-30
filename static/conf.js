$(function () {
	var add = function(event) {
		var input =  $("#addUrl"), url = input.val(), element
		if (url) {
			// fake add it. If it fails ... well it fails !
			element = $(document.createElement("div")).addClass("tracking").html(url)
			$("#configuration").append(element)
			$.ajax({
				type: 'POST',
				url: '/conf',
				data: { url: url },
				success: function(data){
					element.attr("id", data);
					element = null;
				},
				error: function(xhr, type){
					element.addClass("failed")
					element = null
				}
			})
		} else {
			input.addClass("error")
		}
		event.preventDefault()
	},

	remove = function (event) {
		if (window.confirm("Do you reeeeeally want to delete this?")) {
			var element =  $(event.target), 
				id = element.attr("id")
			if (id) {
				$.ajax({
					type: 'DELETE',
					url: '/conf',
					data: { id: id },
					success: function(data){
						element.remove();
						element = null;
					},
					error: function(xhr, type){
						element.addClass("failed")
						element = null
					}
				})
			}
		}
	},

	toggleActive = function (event) {
		var element =  $(event.target), 
			id = element.attr("id")
		if (id) {
			$.ajax({
				type: 'PUT',
				url: '/conf',
				data: { id: id },
				success: function(data){
					element.toggleClass("active")
					element = null;
				},
				error: function(xhr, type){
					element.addClass("failed")
					element = null
				}
			})
		}
	}

	$("#adUrlBtn").on({
		click: add,
		singleTap : add
	})
	$(".tracking").on({
		click : toggleActive,
		singleTap : toggleActive,
		dblclick : remove,
		longTap : remove
	})
})