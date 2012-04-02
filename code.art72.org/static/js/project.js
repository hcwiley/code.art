jQuery.event.add(window, 'load', initProject);

function initProject() {
	$('.media-thumbs').each(
			function(index) {
				var media = $(this);
				var mediaM = $(media).attr('date').split('-')[1];
				var mediaD = $(media).attr('date').split('-')[2]
						.substring(0, 2);
				var dateDiv = $('#' + mediaM + '-' + mediaD);
				console.log(dateDiv.length == 0);
				if (dateDiv.length == 0) {
					dateDiv = $('<div class="dateDiv" id="' + mediaM + '-'
							+ mediaD + '"><h4>' + mediaM + '-' + mediaD
							+ '</h4></div>');
					console.log(dateDiv);
					$('#timeline').append(dateDiv);
				}
				$(media).appendTo($(dateDiv));
			});
	$('.commit').each(
			function(index) {
				var commitM = $(this).attr('date').split('-')[1];
				var commitD = $(this).attr('date').split('-')[2]
						.substring(0, 2);
				var commitTime = $(this).attr('date').split('-')[2].substring(3);
				$($(this).children('p')[0]).text(commitTime+': ');
				var dateDiv = $('#' + commitM + '-' + commitD);
				console.log(dateDiv.length == 0);
				if (dateDiv.length == 0) {
					dateDiv = $('<div class="dateDiv" id="' + commitM + '-'
							+ commitD + '"><h4>' + commitM + '-' + commitD
							+ '</h4></div>');
					console.log(dateDiv);
					$('#timeline').append(dateDiv);
				}
				$(this).appendTo($(dateDiv));
			});
}