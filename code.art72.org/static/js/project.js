jQuery.event.add(window, 'load', initProject);

function initProject(){
    $('.media-thumbs h4').each(function(index) {
        var media = $(this);
        $('.commit-header h4').each(function(index) {
        	var commitM = $(this).text().split('-')[1];
        	var commitD = $(this).text().split('-')[2].substring(0,1);
        	var mediaM = $(media).text().split('-')[1];
        	var mediaD = $(media).text().split('-')[2].substring(0,1);
        	console.log(commitM+'/'+commitD+' :: '+mediaM+'/'+mediaD);
            if(commitM == mediaM && commitD == mediaD) {
                console.log($(this).text().split('-'));
                console.log($(media).text().split('-'));
                $(media).parent().css('background','#cdcdcd');
                $(this).parent().css('background','#cdcdcd');
                // ctx.moveTo($(media).position().left, $(media).position().top);
                // ctx.lineTo($(this).position().left, $(this).position().top);
                // ctx.stroke();
            }
        });
    });
    /*
$('.media-thumbs h4').each(function(index) {
        var media = $(this);
        $('.commit-header h4').each(function(index) {
            if($(this).text().split('-')[1] == $(media).text().split('-')[1] && $(this).text().split('-')[2].substring(0, 1) == $(media).text().split('-')[2].substring(0, 1)) {
                console.log($(this).text().split('-'));
                console.log($(media).text().split('-'));
                $(media).css('background-color', '#cdcdcd');
                $(this).parent().css('background-color', '#cdcdcd');
            }
        });
    });
*/
}