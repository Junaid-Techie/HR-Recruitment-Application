$(document).ready(function () {
    $("#target").validate({
        rules: {
            country_name: {
                required: true,
                minlength: 2
            },
            country_code: {
                required: true,
                minlength: 2
            },
            desc: {
                required: false,
            }
        },
        messages: {
            country_name: {
                required: "Please, enter the country name.",
                minlength: "Country name should be at least 3 characters."
            },
            country_code: {
                required: "Please, enter the country code.",
                minlength: "Country code should be at least 2 characters."
            },
            // desc: {
            //     required: "Please, provide the country description."
            // }
        }
    });
});