$(document).ready(function () {
    $("#target").validate({
        rules: {
            country_name: {
                required: {
                    depends: function(element){
                        if($('#inputState').val() == "none"){
                            //Set predefined value to blank.
                            $('#inputState').val('');
                        }
                        return true;
                    }
                }

            },
            state_name: {
                required: true,
                minlength: 2
            },
            state_desc: {
                required: false,
            }
        },
        messages: {
            country_name: {
                required: "Please, select the country name.",
            },
            state_name: {
                required: "Please, enter the state name.",
                minlength: "State name should be at least 2 characters."
            },
            // state_desc: {
            //     required: "Please, provide the state description."
            // }
        }
    });
});