var performed = false;
var tableinstance;
$(document).ready(function(){
    $("#datatablesSimple").hide();
    $(".input-group-text").hover(function(){
            $(this).css({"text-decoration":"underline", "cursor": "pointer"})});
    console.log(products);
})

function performSearch(){
    if (performed){
        tableinstance.destroy();
    }
    $("#product-list-body").empty();
    $.ajax({
        type: "POST",
        url: "/search/" + $("#searchText").val(),
        success: function(result){
            performed = true;
            generateResult(result)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function generateResult(products){
    var table = $('#product-list-body');
    for(let i=0; i<products.length; i++){
        let product = products[i];
        let row = $("<tr>");

        let col = $('<td>');
        col.append($("<a href=/product/" + product[0]  + '>'+ product[1] + "</a>"));
        row.append(col);
        table.append(row);
    }
    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        tableinstance = new simpleDatatables.DataTable(datatablesSimple);
    }
    $("#datatablesSimple").show();
}