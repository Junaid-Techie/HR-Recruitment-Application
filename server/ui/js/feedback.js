

(function () {


    let FeedbackProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "job" }, { "data": "candidate" },
                { "data": "interview_feedback" }, { "data": "feedback_date" },
                { "data": "interview_type" }, { "data": "next_round" },
                ],
            });
            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    $("#updatebtn").addClass('disabled');
                }
                else {
                    //var rowData = table.rows('.selected').data()[0]['code'];
                    //console.log(rowData);
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    console.log(table.rows('.selected').data()[0]['interviewer_email'])
                    selected_value = table.rows('.selected').data()[0]['interviewer_email']
                    $("#updatebtn").removeClass('disabled');
                    $('#updatebtn').click(function () {
                        selected_value = table.rows('.selected').data()[0]['job']
                        candidate_value = table.rows('.selected').data()[0]['candidate_email']
                        console.log(selected_value)
                        var txn = document.getElementById('txn')
                        txn.value = selected_value + '#' + candidate_value;
                        $('#target').attr('action', '/hroffice/editschedule');
                        $('#target').attr('method', 'post')
                        $("#target").submit();
                    });

                }
            });

            $('#jobcode').change(function () {
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                var jobcode = $('#jobcode').val();

                $.ajax({
                    url: "/hroffice/api/feedback/shortlistapplication/job/" + jobcode,
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
                        $("#Candidate").empty();

                        $("#Candidate").append("<option value=''>---Select---</option>");
                        for (var k = 0; k < len; k++) {
                            var name = dataObj[k]['first_name'] + ' ' + dataObj[k]['last_name'];
                            var id = dataObj[k]['email'];
                            $("#Candidate").append("<option value='" + id + "'>" + name + "</option>");
                        }

                        console.log(dataObj);
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(errorThrown);
                    }
                });
            });

            $('#Candidate').change(function () {
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                var Candidate = $('#Candidate').val();
                var job = document.getElementById('jobcode').value;
                $.ajax({
                    url: "/hroffice/api/feedback/interviewtype?job=" + job + '&candidate=' + Candidate,
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
                        interview_type = dataObj[0]['interview_type'];
                        round_number = dataObj[0]['round_number'];
                        console.log(dataObj);
                        //document.getElementById('interview_type').value = interview_type;
                        $("#interview_type").html("<option value='" + interview_type + "'>" + interview_type + " </option>");
                        $("#round_number").html("<option value='" + round_number + "'>" + round_number + " </option>");
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
                    url: "/hroffice/api/feedback/addrecord",
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

            // $(document).ready(function () {
            //     $('#updsubmit').click(function (e) {
            //         var frm = $('#target')[0];
            //         var frmData = new FormData(frm);
            //         $.ajax({
            //             url: "/hroffice/api/scheduler/reschedule",
            //             type: 'PUT',
            //             cache: false,
            //             processData: false,
            //             contentType: false,
            //             timeout: 600000,
            //             data: frmData,
            //             success: function (data, textStatus, jQxhr) {
            //                 $('#message').html(data.message);
            //                 console.log(data);
            //             },
            //             error: function (jqXhr, textStatus, errorThrown) {
            //                 console.log(errorThrown);
            //             }
            //         });
            //     });
            // });

        },
        loadData: function (successCallback) {
            url = '/hroffice/api/feedback/fetchrecords';
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
        FeedbackProfile.loadData(FeedbackProfile.populateDataTable);
    });
})();

