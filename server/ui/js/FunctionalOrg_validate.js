$(document).ready(function () {
    $("#target").validate({
        rules: {
            org_name: {
                required: true,
                minlength: 2
            },
            orgemail: {
                required: true,
            },
            ccemail: {
                required: true,
            },
        },
        messages: {
            org_name: {
                required: "Please, enter the functional organisation name.",
                minlength: "functional organisation name should be at least 2 characters."
            },
            orgemail: {
                required: "Please, enter the organisation email address.",
            },
            ccemail: {
                required: "Please, enter the organisation cc email address.",
            },
        }
    });
});