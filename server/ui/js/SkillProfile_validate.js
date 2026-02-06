$(document).ready(function () {
    $("#target").validate({
        rules: {
            skill_name: {
                required: true,
                minlength: 2
            },
            skill_desc: {
                required: false,
            }
        },
        messages: {
            skill_name: {
                required: "Please, enter the Skill.",
                minlength: "Skill should be at least of 2 characters."
            },
            // skill_desc: {
            //     required: "Please, provide the skill description.",
            // }
        }
    });
});