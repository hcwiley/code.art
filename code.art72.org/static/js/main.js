jQuery.event.add(window, 'load', init);

function showPostForm() {
    $('#post_form').add('#right-nav').animate({
        height : 500,
    }, 400).css('display', 'block');
}

var changing = false;
var animateDelay = 400;
function watchURLChange() {
    var tmploc = window.location + "";
    tmploc = tmploc.split('/');
    tmploc = tmploc[tmploc.length - 1];
    if(changing) {
        window.setTimeout("watchURLChange();", (animateDelay) * 2);
    } else {
        if(loc !== tmploc) {
            changePage(tmploc);
        } else {
            window.setTimeout("watchURLChange();", 100);
        }
    }
}

function changePage(url) {
    if((location.pathname.match("profile") && url.match("profile") == null) || (!location.pathname.match("profile") && url.match("profile"))) {
        window.location = url;
    }
    changing = true;
    $('#main').animate({
        opacity : 0
    }, animateDelay);
    window.setTimeout(function() {
        $.get(url, function(data) {
            $('#main').html(data);
            $('#main').animate({
                opacity : 1
            }, animateDelay);
            if(history && history.pushState) {
                history.pushState({
                    module : "leave"
                }, "code.art ajax", url);
            }
            init();
            if(location.pathname.match('profile'))
                initProfile();
        });
    }, animateDelay / 1.5);
}

function init() {
    changing = false;
    //loc == current page
    loc = window.location + "";
    loc = loc.split('/');
    loc = loc[loc.length - 1];
    // watchURLChange();
    // $('*:not(a)').unbind();
    $('#new-post').click(function() {
        showPostForm();
        $(this).hide(400);
    });
    $('#right-nav').mouseleave(function() {
        if($('#post_form').css('display') == 'block') {
            $('#post_form').animate({
                height : 0,
            }, 400).css('display', 'none');
            $('#right-nav').animate({
            }, 400);
            $('#new-post').show(400);
        }
    });
    $('.media-thumbs > img').click(function() {
        var src = $(this).attr('video');
        if(src != null || src == "") {
            var open = $(this).siblings('iframe');
            if(open.length == 0) {
                open = $(this).siblings('video');
                $(open).children("source").attr('src', src);
            }
            $(open).attr('src', src);
            $(open).show();
            $(this).parent().addClass('open');
            $(this).hide();
            $(this).siblings('h6').hide();
        } else {
            src = $(this).attr('image');
            var open = $(this).siblings('img');
            $(open).attr('src', src)
            $(open).css('display','inline');
            $(this).parent().addClass('open');
            $(this).hide();
            $(this).siblings('h6').hide();
        }
        $(open).click(function() {
            $(open).click(function() {
                $(this).parent().removeClass('open');
                $(this).hide();
                $(this).siblings('h6').show();
                $(this).siblings('.mini').show();
                $(open).unbind();
            });
        });
    });
    /*
    $('a:not(.no-link)').each(function() {
        $(this).unbind('click');
        if($(this).attr('href').match(location.host) == null && $(this).attr('href').match("http") != null) {
            // console.log($(this).attr('href'));
            return;
        }
        $(this).click(function(e) {
            e.preventDefault();
            var url = $(this).attr('href');
            changePage(url);
        });
    });
    */
}