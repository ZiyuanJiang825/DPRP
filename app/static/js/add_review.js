$(document).ready(function(){
    if (msg != '') {
        $("#alert-msg").show();
    }
    if (msg == "Please Login First!") {

        setTimeout("window.location.href='/login'", 1000);
    }
})

function showProducts(val) {
    $.ajax({
        type: "POST",
        url: "/search/" + val,
        success: function(products){
            let product_list = [];
            for(let i=0; i<products.length; i++){
                let product = products[i];
                product_list.push(product[1]);
            }
            $( "#inputProductName" ).autocomplete({
                source: product_list
            });
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}