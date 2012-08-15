// all.js

var highlight = function () {
	$("circle").css("fill", "#CCC")
	var id = $(this).attr("id").substring(3)
	$("#circle_" + id).css("fill", "red")
}

$("tr").on({
	click : highlight,
	tap : highlight
})

