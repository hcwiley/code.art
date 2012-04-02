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
		$($('#tmp').attr('orig')).replaceWith(me);
		$('#id_use_git_blurb').attr('checked', false);
		$(me).parent('form').submit();
		$('.editting').removeClass('editting');
		$('#editting_note').removeClass('editting');
	}
}

function initProfile() {
	$('.editable').unbind(); 
	$('.project-selector').children('.a-project').click(function() {
		var title = $(this).attr('media');
		$('#editting_note').addClass('editting');
		var selected = true;
		if($(this).attr('class').match('current')) {
			selected = false;
		} else {
			$(this).addClass('added');
		}
		// console.log(selected);
		$('#' + $(this).attr('form') + ' [name=media] option').each(function() {
			if($(this).text() == title) {
				if(selected)
					$(this).attr('selected', selected);
				else
					$(this).removeAttr('selected');
			}

		});
		// console.log($('#'+$(this).attr('form')));
		$('#save-menu').show();
		$('#' + $(this).attr('form')).addClass('modified');
	});
	$('.editable').mousedown(function(event) {
		// console.log(event.which);
		if(event.which == 3) {
			$('body').attr('oncontextmenu', "return false");
			if($('.editting').length < 1) {
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
	$('[name=media] option').each(function() {
		var title = $(this).parent().siblings('#id_title').val()
		var projects = $('.a-project[title="' + title + '"]');
		for(var i = 0; i < projects.length; i++) {
			if($(this).text() == $(projects[i]).attr('media') && $(this).attr('selected') == "selected") {
				$(projects[i]).addClass('current');
			}
		}
	});
	$('#add_project').click(function() {
		$('#new-project').show();
	});
	$('#save').click(function() {
		$('.modified').each(function() {
			$.post($(this).attr('action'), $(this).serialize(), function(data) {
				$('#main').html(data);
				initProfile();
				init();
			});
		});
	});
	$('#cancel').click(function() {
		window.locaiton = window.location;
	})
}