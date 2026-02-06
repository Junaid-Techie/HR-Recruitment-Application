
$(document).ready(function () {
    $("#target").validate({
        rules: {
            emp_id: {
                required: true,
                minlength: 5,
                number: true,
            },
            first_name: {
                required: true,
                minlength: 1
            },
            middle_name: {
                required: true,
                minlength: 0
            },
            last_name: {
                required: true,
                minlength: 1
            },
            designation: {
                required: true,
                minlength: 4
            },
            phone: {
                required: true,
                minlength:10,
                phonevalidation: true
            },
            email: {
                required: true,
            },
            location: {
                required: true
            },
            shift_start_time: {
                required: true,
            },
            shift_end_time: {
                required: true,
            }
        },
        messages: {
            emp_id: {
                required: "Please enter the Employee ID.",
                minlength: "Employee ID should be at least 5 characters.",
                number: "Employee ID must be a number."
            },
            first_name: {
                required: "Please, enter the first name.",
                minlength: "first name should be at least of 1 character. "
            },
            middle_name: {
                required: "Please, enter the middle name.",
                minlength: "middle name should be at least of 1 character. "
            },
            last_name: {
                required: "Please, enter the last name.",
                minlength: "last name should be at least of 1 character. "
            },
            designation: {
                required: "Please, enter the designation.",
                minlength: "designation should be at least of 4 character. "
            },
            phone: {
                required: "Please, enter the phone number.",
            },
            email: {
                required: "Please, enter the email address.",
            },
            location: {
                required: "Please, enter the location."
            },
            shift_start_time: {
                required: "Please, select the start shift time.",
            },
            shift_end_time: {
                required: "Please select the end shift time.",
            }
        }
    });
    $.validator.addMethod("phonevalidation",
               function(value, element) {
                       return /^[A-Za-z\d=#$%@_ -]+$/.test(value);
               },
       "Please enter a valid phone number."
       );
});
