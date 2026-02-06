$(document).ready(function () {
    $("#target").validate({
        rules: {

            code: {
                required: true
            },
            resume: {
                required: true
            },
        },
        messages: {
            code: {
                required: "Please, select the Job Code."
            },
            resume: {
                required: "Please, uploade the resumes."
            }
        }
    });
});