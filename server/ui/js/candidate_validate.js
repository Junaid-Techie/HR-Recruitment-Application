$(document).ready(function () {
    $("#target").validate({
        rules: {

            code: {
                required: truev
            },
            first_name: {
                required: true,
                minlength: 2
            },
            middle_name: {
                required: true,
                minlength: 3
            },
            last_name: {
                required: true,
                minlength: 2
            },
            notice_period: {
                required: true,
            },
            experience: {
                required: true
            },
            education: {
                required: true
            },
            phone: {
                required: true
            },
            email: {
                required: true
            },
            primary_skill: {
                required: true
            },
            secondary_skill: {
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
            first_name: {
                required: "Please, enter the first name.",
                minlength: "first name should be at least of 2 character. "
            },
            middle_name: {
                required: "Please, enter the middle name.",
                minlength: "middle name should be at least of 3 character. "
            },
            last_name: {
                required: "Please, enter the last name.",
                minlength: "last name should be at least of 2 character. "
            },
            notice_period: {
                required: "Please, select the notice period."
            },
            experience: {
                required: "Please, select the years of experience."
            },
            education: {
                required: "Please, select the education qualification."
            },
            phone: {
                required: "Please, enter the phone number."
            },
            email: {
                required: "Please, enter the email address."
            },
            primary_skill: {
                required: "Please, select the primary skill."
            },
            secondary_skill: {
                required: "Please, select the secondary skill."
            },
            resume: {
                required: "Please, uploade the resume."
            }
        }
    });
});