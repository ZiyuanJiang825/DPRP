$(document).ready(function(){
    let table = $('<table>')
    let row = $('<tr>')
    row.append($('<td>').text('Title'))
    row.append($('<td>').text('Product'))
    table.append(row);

    for(let i=0; i<reviews.length; i++){
        review = reviews[i]
        row = $('<tr>').css({"text-decoration":"None"})
        row.append($('<td>').text(review[3]))
        row.append($('<td>').text(review[4]))
        $(row).hover(function(){
            $(this).css({"text-decoration":"underline", "cursor": "pointer"})
        },function() {
            $(this).css({"text-decoration":"none", "cursor":"default"})
          }
        )
        $(row).on('click', function(event) {
            event.preventDefault();
            window.location = "/review/" + reviews[i][1] + '/' + reviews[i][0]
        });
        table.append(row);
    }
    $('#reviews').append(table);
})