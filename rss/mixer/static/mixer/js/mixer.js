function loadData(data) {
    $("#feed_count").html(data['feed_count'])
    $("#feed_list").html('')
    $.each(data['feed_list'], function(feed_slug, feed_link) {
        $("#feed_list").append(
            $('<li/>').append(
                $('<a/>', {'href': feed_slug, text: feed_link}),
                $('<a/>', {'class': 'feed_delete', 'href': '/delete/'+feed_slug}).append(
                    $('<i/>', {'class': 'glyphicon glyphicon-minus-sign', 'rel': 'tooltip', 'data-toggle': 'tooltip', 'data-placement': 'right'}))));
    });

    $("#item_count").html(data['item_count'])
    $("#item_list").html('')
    $.each(data['item_list'], function(index, item){
        $("#item_list").append(
            $('<div/>').append(
                $('<h3/>').append(
                    $('<a/>', {'href': item.link, text: item.title})),
                $('<p/>', {text: item.summary})
                $('<p/>', {text: 'Date: '}.append(
                    $('<em/>', {text: item.published})))));
    });

}

$(document).ready(function() {
    $('*[rel="tooltip"]').tooltip();
    $('#taskDescription').tab();
});

$(document).on('click', '#add_feed', function(event) {
    var $form = $(this).closest('form');
    $.ajax({
        url: "/",
        type: 'POST',
        data: $form.serialize()
    }).done(function(data) {
        $("input[type=url]").val('');
        loadData(data);
    })
    event.preventDefault();
});

$(document).on('click', ".feed_delete", function(event) {
    $.ajax({
        url: $(this).attr('href'),
        type: 'GET',
        // enable cache since a GET to a delete URL redirects and
        // we don't want to cache the redirected page
        cache: false
    }).done(function(data) {
        loadData(data);
    });
    event.preventDefault();
});
