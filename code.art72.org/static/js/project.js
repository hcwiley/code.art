jQuery.event.add(window, 'load', initProject);

function initProject() {
	$('.media-thumbs').each(
			function(index) {
				var media = $(this);
				var mediaY = $(media).attr('date').split('-')[0];
				var mediaM = $(media).attr('date').split('-')[1];
				var mediaD = $(media).attr('date').split('-')[2]
						.substring(0, 2);
				var dateDiv = $('#' + mediaM + '-' + mediaD);
				if (dateDiv.length == 0) {
					dateDiv = $('<div class="dateDiv" id="' + mediaM + '-'
							+ mediaD + '"><h4>' + mediaM + '-' + mediaD + '-' + mediaY
							+ '</h4></div>');
					$('#timeline').append(dateDiv);
				}
				$(media).appendTo($(dateDiv));
			});
	$('.commit').each(
			function(index) {
				var commit = $(this);
				var commitY = $(commit).attr('date').split('-')[0];
				var commitM = $(commit).attr('date').split('-')[1];
				var commitD = $(commit).attr('date').split('-')[2]
						.substring(0, 2);
				var commitTime = $(commit).attr('date').split('-')[2].substring(3);
				$($(commit).children('p')[0]).text(commitTime+': ');
				var dateDiv = $('#' + commitM + '-' + commitD);
				if (dateDiv.length == 0) {
					dateDiv = $('<div class="dateDiv" id="' + commitM + '-'
							+ commitD + '"><h4>' + commitM + '-' + commitD + '-' + commitY
							+ '</h4></div>');
					$('#timeline').append(dateDiv);
				}
				$(commit).appendTo($(dateDiv));
			});
}
