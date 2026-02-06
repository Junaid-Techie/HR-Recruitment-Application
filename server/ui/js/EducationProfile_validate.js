$(document).ready(function () {
    $("#target").validate({
        rules: {
            qualification: {
                required: true,
                minlength: 2
            },
            university: {
                required: true,
                minlength: 2
            },
            specialisation: {
                required: true,
                minlength: 2
            },
            qualification_description: {
                required: true,
            }
        },
        messages: {
            qualification: {
                required: "Please, enter the qualification.",
                minlength: "Qualification should be at least 2 characters."
            },
            university: {
                required: "Please, enter the university name.",
                minlength: "University name should be at least 2 characters."
            },
            specialisation: {
                required: "Please, enter the specialisation.",
                minlength: "Specialisation should be at least 2 characters."
            },
            qualification_description: {
                required: "Please, provide the qualification description."
            }
        }
    });
});