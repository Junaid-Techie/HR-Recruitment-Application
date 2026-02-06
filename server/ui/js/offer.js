(function () {


    let OfferProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "job" }, { "data": "applicant" },
                { "data": "join_date" }, { "data": "comments" },
                ],
            });

            $('#jobcode').change(function () {
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                var jobcode = $('#jobcode').val();

                $.ajax({
                    url: "/hroffice/api/offer/offered_applicants/job/" + jobcode,
                    type: 'GET',
                    cache: false,
                    processData: false,
                    contentType: false,
                    timeout: 600000,
                    data: frmData,
                    beforeSend: function () {
                        $('#loading').show();
                    },
                    complete: function () {
                        $('#loading').hide();
                    },
                    success: function (dataObj, textStatus, jQxhr) {
                        //$('#message').html(data.message);
                        var len = dataObj.length;
                        $("#applicant").empty();

                        $("#applicant").append("<option value=''>---Select---</option>");
                        for (var k = 0; k < len; k++) {
                            var name = dataObj[k]['first_name'] + ' ' + dataObj[k]['last_name'];
                            var id = dataObj[k]['email'];
                            $("#applicant").append("<option value='" + id + "'>" + name + "</option>");
                        }

                        console.log(dataObj);
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(errorThrown);
                    }

                });
            });
            $('#submit').click(function (e) {
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: "/hroffice/api/offer/addrecord",
                    type: 'POST',
                    cache: false,
                    processData: false,
                    contentType: false,
                    timeout: 600000,
                    data: frmData,
                    beforeSend: function () {
                        $('#loading').show();
                    },
                    complete: function () {
                        $('#loading').hide();
                    },
                    success: function (data, textStatus, jQxhr) {
                        if (data.status == 'success') {
                            $('#message').html('');
                            $('#errormessage').html('');
                            $('#message').html(data.message);
                        } else {
                            $('#message').html('');
                            $('#errormessage').html('');
                            $('#errormessage').html(data.message);
                        }
                        console.log(data);
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(errorThrown);
                    }
                });
            });
        },
        loadData: function (successCallback) {
            url = '/hroffice/api/offer/getrecords';
            $.ajax({
                type: 'GET',
                url: url,
                contentType: "application/json",
                dataType: 'json',
                beforeSend: function () {
                    $('#loading').show();
                },
                complete: function () {
                    $('#loading').hide();
                },
                success: function (data) {

                    myJsonData = data;
                    successCallback(myJsonData);
                },
                error: function (e) {
                    console.log("There was an error with your request...");
                    console.log("error: " + JSON.stringify(e));
                }
            });
        }
    };
    $('#target').ready(function () {
        $.noConflict();
        OfferProfile.loadData(OfferProfile.populateDataTable);
    });
})();

