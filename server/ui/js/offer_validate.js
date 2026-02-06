$(document).ready(function () {
    $("#target").validate({
        rules: {
            job: {
                required: true,
            },
            applicant: {
                required: true,
            },
            comments: {
                required: true,
                minlength: 5
            },
            join_date: {
                required: true,
            },
            offer_attachment: {
                required: true,
            },
        },
        messages: {
            job: {
                required: "please, select the Job Code.",
            },
            applicant: {
                required: "Please, select the candidate.",
            },
            comments: {
                required: "please, provide comments on the offer.",
                minlength: "comments should be at least 5 characters."
            },
            join_date: {
                required: "please, select the join date.",
            },
            offer_attachment: {
                required: "please, upload the offer letter.",
            },
        }
    });
});