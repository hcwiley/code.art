jQuery.event.add(window, 'load', init);

function showPostForm(){
    $('#post_form').add('#right-nav').animate({
        height: 500,
    }, 400).css('display', 'block');
}

function init(){
    $('#new-post').click(function(){
        showPostForm();
        $(this).hide(400);
    });
    $('#right-nav').mouseleave(function(){
        if ($('#post_form').css('display') == 'block') {
            $('#post_form').animate({
                height: 0,
            }, 400).css('display', 'none');
            $('#right-nav').animate({
            }, 400);
            $('#new-post').show(400);
        }
    });
    $('.media-thumbs > img').click(function(){
		var src = $(this).attr('video');
		$(this).siblings('iframe').attr('src', $(this).attr('video')).show();
		$(this).parent().addClass('video');
		$(this).hide();
		$(this).siblings('h6').hide();
	});
}
