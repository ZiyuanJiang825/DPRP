
$(document).ready(function(){
    var table = $('#review-list-body');
    for(let i=0; i<reviews.length; i++){
        review = reviews[i];
        let row = $("<tr>");

        let col = $('<td>');
        col.append($("<a href=/review/" + reviews[i][1] + '/' + reviews[i][0] + '>'+ review[3] + "</a>"));
        row.append(col);

        row.append($('<td>').text(review[4]));
        row.append($('<td>').text(review[9]));
        let action_col = $("<td>");
        action_col.append($("<a class=\"btn btn-datatable btn-icon btn-transparent-dark\" href=\"edit/" + review[0] + "\"><i data-feather=\"edit\"></i></a>"));
        action_col.append($("<span>&nbsp&nbsp&nbsp</span>"));
        action_col.append($("<a class=\"btn btn-datatable btn-icon btn-transparent-dark\" href=\"#!\"><i data-feather=\"trash-2\"></i></a>"));
        row.append(action_col);
        table.append(row);
    }
    feather.replace();
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }
})