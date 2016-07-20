function rescroll() {
	$('.scrollable-data').show();
	// hide everything that is out of bound
	$('.scrollable-data').filter(function(index) {
		console.log($(this).position().top, $(window).height() + $(window).scrollTop());
		return ($(this).position().top > $(window).height() + $(window).scrollTop());
	}).hide();

}

$(window).scroll(function() {
	rescroll();
  console.log('rescroll');
});

rescroll();
