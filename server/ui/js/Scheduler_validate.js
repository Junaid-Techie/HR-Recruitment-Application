$(document).ready(function () {
    $("#target").validate({
        // focusInvalid: false,
        // invalidHandler: $("input").focus(function () {
        //     $this.focus;
        // }),
        rules: {
            job: {
                required: true,
            },
            candidate: {
                required: true,
            },
            interviewer_name: {
                required: true,
            },
            interviewer_email: {
                required: true,
            },
            interviewer_phone: {
                required: true,
            },
            scheduled_datetime: {
                required: true,
            },
            round_number: {
                required: true,
                number: true,
            },
            interview_type: {
                required: true,
            },
            interview_channel: {
                required: true,
            },
        },
        messages: {
            job: {
                required: "Please, select the Job Code.",
            },
            candidate: {
                required: "Please, select the candidate.",
            },
            interviewer_name: {
                required: "Please, enter the name.",
            },
            interviewer_email: {
                required: "Please, enter the email address.",
            },
            interviewer_phone: {
                required: "Please, enter the phone number.",
            },
            scheduled_datetime: {
                required: "Please, select the date and time to schedule the interview.",
            },
            round_number: {
                required: "Please, select the round number.",
                number: "this should be numeri.",
            },
            interview_type: {
                required: "Please select the interview type.",
            },
            interview_channel: {
                required: "Please select the mode of interview.",
            },
        }
    });
});