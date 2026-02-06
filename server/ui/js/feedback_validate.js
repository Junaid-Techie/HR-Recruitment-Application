$(document).ready(function () {
    $("#target").validate({
        rules: {
            job: {
                required: true,
            },
            schedule: {
                required: true,
            },
            interview_feedback: {
                required: true,
                minlength: 5
            },
            interview_type: {
                required: true,
            },
            interview_feedback_attachment: {
                required: true,
            },
            round_number: {
                required: true,
            },
            next_round: {
                required: true,
            }
        },
        messages: {
            job: {
                required: "please, select the Job Code.",
            },
            schedule: {
                required: "Please, select the scheduled candidate.",
            },
            interview_feedback: {
                required: "please, provide feedback on the interview.",
                minlength: "interview feedback should be at least 5 characters."
            },
            interview_type: {
                required: "please, select the type of interview.",
            },
            interview_feedback_attachment: {
                required: "please, upload the feedback attachment.",
            },
            round_number: {
                required: "please, select the round number.",
            },
            next_round: {
                required: "please, select the next round.",
            }
        }
    });
});