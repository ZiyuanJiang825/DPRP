$(document).ready(function(){
    if (msg !== '') {
        $("#alert-msg").show();
    }
    if (msg === "Please Login First!") {

        setTimeout("window.location.href='/login'", 1000);
    } else if (msg === "Please fill out the form !" || msg === "You have successfully edited a review!" || msg === "Edit failed! You have not purchased this item!"){
        setTimeout("window.location.replace('/reviews/edit/' + review['Id'])", 500);
    }
    var form = document.getElementById('editReviewForm');
    form.action = '/reviews/edit/' + review['Id'] + '/submit';

    if (review != '') {
        $("#inputTitle").val(review['Title']);
        $("#inputProductName").val(review['ProductName']);
        $("#inputReview").val(review['Review']);
        $("#inputPros").val(review['Pros']);
        $("#inputCons").val(review['Cons']);
        $("#inputRating").val(review['Rating']);
    }

})

$('#editReviewForm').submit(function(e) {
    $(':disabled').each(function(e) {
        $(this).removeAttr('disabled');
    })
});

$('#discardReview').click(function(){
    window.location.replace('/reviews/edit/' + review['Id'])
})
