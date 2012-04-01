jQuery.event.add(window, 'load', initProject);

function initProject() {
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
}