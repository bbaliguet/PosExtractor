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
					element.attr("id", data)
						.append('<a href="#" class="pull-right" title="delete">' + 
            					'<i class="icon-remove"></i></a>')
						.
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
			// handle link click. REFACTOR ME
			if (!id) {
				element = element.parents("div.tracking")
				id = element.attr("id")
			}
			if (id) {
				// optimistic approach : everything 's gonna be alright
				element.remove()
				$.ajax({
					type: 'DELETE',
					url: '/conf?id=' + id,
					success: function(data){
						element = null;
					},
					error: function(xhr, type){
						// something wen't wrong : put it back in display
						$("#configuration").append(element)
						element.addClass("failed")
						element = null
					}
				})
			}
		}
		event.preventDefault();
		return false;
	},

	toggleActive = function (event) {
		var element =  $(event.target), 
			id = element.attr("id")
		if (id) {
			// optimitic
			element.toggleClass("active")
			$.ajax({
				type: 'PUT',
				url: '/conf',
				data: { id: id },
				success: function(data){
					// adjust on server answer
					if (data == "1") {
						element.addClass("active")
					} else {
						element.removeClass("active")
					}
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
		longTap : remove
	})
	$(".tracking a").on("click", remove)
	
})