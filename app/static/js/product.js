$(document).ready(function(){
    reviewBody = $("#product-reviews-content");
    total_rating = 0;
    $("#review-number").text(reviews.length);
    for(let i=0; i<reviews.length; i++) {
        appendReview(reviews[i]);
    }
    $("#avg-rating").text((total_rating / reviews.length).toFixed(2));
})

function appendReview(details){
    total_rating += details[4];
    let card = $("<div class='card' style='margin-bottom: 20px;'>");
    let card_header = $("<div class='card-header'>");
    let card_body = $("<div class='card-body'>");
    let card_username = $("<h6 class='small text-muted fw-500'>");
    let review_content = $("<div class='border rounded' style='padding: 5px; margin-bottom: 10px;'>");
    let review_pro_con = $("<div class='border rounded' style='padding: 5px; margin-bottom: 10px;'>");
    let pro_bold = $("<span class='fw-bolder'>");
    let con_bold = $("<span class='fw-bolder'>");
    pro_bold.text("Pros: ");
    con_bold.text("Cons: ");
    review_pro_con.append(pro_bold);
    review_pro_con.append(details[2]);
    review_pro_con.append($("<br>"));
    review_pro_con.append(con_bold);
    review_pro_con.append(details[3]);

    let review_rating = $("<div class='border rounded' style='padding: 5px; margin-bottom: 10px;'>");
    let rating_bold = $("<span class='fw-bolder'>");
    rating_bold.text("Rating: ");
    review_rating.append(rating_bold);
    review_rating.append(details[4]);
    review_content.text(details[1]);

    let card_verify = $("<span class='badge bg-success' style='margin-left: 10px;'>");
    card_verify.text("Verified by blockchain");
    card_username.text("By " + details[5]);
    card_username.append(card_verify);
    card_body.append(review_content);
    card_body.append(review_pro_con);
    card_body.append(review_rating);
    card_body.append(card_username);
    card_header.text(details[0]);

    card.append(card_header);
    card.append(card_body);
    reviewBody.append(card);
}
