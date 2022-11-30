$(document).ready(function(){
    $("#verify").click(function(event) {
        console.log(review['Id'])
        event.preventDefault();
        $.ajax({
        type: "POST",
        url: "/review/verify",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify({
            Id: review['Id']
        }),
        success: function(result){
            console.log('a')
            alert(result)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
        });
    });
})