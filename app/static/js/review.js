$(document).ready(function(){
    historyBody = $("#reviewTimeline");
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

    for(let i=0; i<editHistory.length; i++) {
        appendHistory(editHistory[i]);
    }
})

function appendHistory(details){
    let timelineItem = $("<div class='timeline-item'>");
    let timelineMarker = $("<div class='timeline-item-marker'>");
    let timelineMarkerText = $("<div class='timeline-item-marker-text'>");
    let timelineMarkerIndicator = $("<div class='timeline-item-marker-indicator'><i data-feather='check'>");
    let timelineContent = $("<div class='timeline-item-content'>");
    timelineMarkerText.text(details[2]);
    timelineContent.text("Tx Hash is: " + details[0]);
    timelineMarker.append(timelineMarkerText);
    timelineMarker.append(timelineMarkerIndicator);
    timelineItem.append(timelineMarker);
    timelineItem.append(timelineContent);


    historyBody.append(timelineItem);
}