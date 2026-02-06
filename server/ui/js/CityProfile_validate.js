$(document).ready(function () {
    $("#target").validate({
        rules: {
            country_name: {
                required: {
                    depends: function(element){
                        if($('#inputCountry').val() == "none"){
                            //Set predefined value to blank.
                            $('#inputCountry').val('');
                        }
                        return true;
                    }
                }
            },
            state_name: {
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
            city_name: {
                required: true,
                minlength: 2
            },
            address: {
                required: true,
                minlength: 10
            },
            city_desc: {
                required: false,
            }
        },
        messages: {
            country_name: {
                required: "Please, select the country name.",
            },
            state_name: {
                required: "Please, select the state name.",
            },
            city_name: {
                required: "Please, enter the city name.",
                minlength: "city name should be at least 2 characters."
            },
            city_address: {
                required: "Please, enter the address.",
                minlength: "address should be at least 10 characters."
            },
            // city_desc: {
            //     required: "Please, provide the city description."
            // }
        }
    });
});