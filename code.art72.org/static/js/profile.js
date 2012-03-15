jQuery.event.add(window, 'load', initProfile);

function useGit(b) {
	if(b == 1) {
		me = $('#id_use_git_blurb');
		me.attr('checked', true);
		$(me).parent('form').submit();
	}else{
		me = $('#id_use_git_blurb');
		me.attr('checked', false);
		$(me).parent('form').submit();
	}
}

function initProfile() {
	$('.editable').mousedown(function(event) {
		console.log(event.which);
		if(event.which == 3) {
			$('body').attr('oncontextmenu',"return false");
			if($('.editting').length < 1) {
				$('#editting_note').addClass('editting');
				var orig = $(this).clone();
				var input = $('#id_' + $(this).attr('id')).clone().attr('id', 'tmp').attr('orig', '#id_' + $(this).attr('id')).addClass('editting');
				console.log(input);
				$(this).replaceWith(input);
				window.setTimeout(function() {
					$(document).mousedown(function(event) {
						console.log(event.which);
						if(event.which == 3) {
							if($('.editting').length > 0) {
								var me = $('#tmp');
								console.log('save me ' + me);
								$($('#tmp').attr('orig')).replaceWith(me);
								$('#id_use_git_blurb').attr('checked', false);
								$(me).parent('form').submit();
								$('.editting').removeClass('editting');
								$('#editting_note').removeClass('editting');
								$(document).unbind('mousedown');
							}
						}
					});
				}, 1000);
			}
		}
	});
}