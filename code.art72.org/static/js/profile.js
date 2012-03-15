jQuery.event.add(window, 'load', initProfile);

function useGit(b) {
	if(b == 1) {
		me = $('#id_use_git_blurb');
		me.attr('checked', true);
		$(me).parent('form').submit();
	} else {
		me = $('#id_use_git_blurb');
		me.attr('checked', false);
		$(me).parent('form').submit();
	}
}

function sendEdits() {
	if($('.editting').length > 0) {
		var me = $('#tmp');
		console.log('save me ' + me);
		$($('#tmp').attr('orig')).replaceWith(me);
		$('#id_use_git_blurb').attr('checked', false);
		$(me).parent('form').submit();
		$('.editting').removeClass('editting');
		$('#editting_note').removeClass('editting');
	}
}

function initProfile() {
	$('.editable').mousedown(function(event) {
		console.log(event.which);
		if(event.which == 3) {
			$('body').attr('oncontextmenu', "return false");
			if($(this).attr('class').match('media-thumb')) {
				// $('.editable').unbind();
				$(this).next('.project-selector').removeClass('hidden');
				$('#editting_note').addClass('editting');
				$('#editting_note > h5').text('click the project you want to add this to');
				$(this).next('.project-selector').children('.project').click(function() {
					var title = $(this).attr('media');
					var selected = true;
					if($(this).attr('class').match('current'))
						selected = false;
					console.log(selected);
					$('#id_media option').each(function() {
						console.log($(this));
						if($(this).text() == title){
							if(selected)
								$(this).attr('selected', selected);
							else
								$(this).removeAttr('selected');							
						}
						
					});
					$('form').submit();
				});
			} else if($('.editting').length < 1) {
				$('#editting_note').addClass('editting');
				var orig = $(this).clone();
				var input = $('#id_' + $(this).attr('id')).clone().attr('id', 'tmp').attr('orig', '#id_' + $(this).attr('id')).addClass('editting');
				$(this).replaceWith(input);
				window.setTimeout(function() {
					$(document).mousedown(function(event) {
						if(event.which == 3) {
							sendEdits();
							$(document).unbind('mousedown');
						}
					});
					console.log
					if(!$('#tmp').is('textarea')) {
						$(document).keydown(function(event) {
							if(event.which == 13) {
								sendEdits();
							}
						});
					}
				}, 1000);
			}
		}
	});
	$('#id_media option').each(function() {
		var projects = $('.project');
		for(var i = 0; i < projects.length; i++) {
			if($(this).text() == $(projects[i]).attr('media') && $(this).attr('selected') == "selected")
				$(projects[i]).addClass('current');
		};
	});
}