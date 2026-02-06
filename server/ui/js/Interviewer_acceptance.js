/*
$.getScript('https://code.jquery.com/jquery-3.3.1.js', function () {
    // script is now loaded and executed.
    // put your dependent JS here.
});
$.getScript('https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js', function () 
{
    // script is now loaded and executed.
    // put your dependent JS here.
});
*/

(function () {


    let SchedulerProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "job" }, { "data": "candidate" }, { "data": "candidate_email" },
                { "data": "interviewer_name" }, { "data": "interviewer_email" }, { "data": "interview_type" }, { "data": "scheduled_datetime" },
                {
                    "data": "job",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/jobpreviewfile?code=' + row.job + '">View</a></span>';
                    }
                },
                {
                    "data": "job",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/candidatepreviewfile?code=' + row.job + '&email=' + row.candidate_email + '">View</a></span>';
                    }
                },
                {
                    "data": "interviewer_acknowledgement",
                    "sWidth": "5%",
                    "mRender": function (data, type, row, meta) {
                        status = row.interviewer_acknowledgement;
                        options = ""
                        id = meta.row + meta.settings._iDisplayStart + 1;
                        if (status == 'Yet to Confirm') {
                            options = "<option value=" + status + " selected>" + status + "</option><option value='Accepted'>Accepted</option><option value='Rejected'>Rejected</option><option value='Propose for Reschedule'>Propose for Reschedule</option>"
                        } else if (status == 'Accepted') {
                            options = "<option value=" + status + " selected>Accepted</option><option value='Rejected'>Rejected</option><option value=\"Yet to Confirm\">Yet to Confirm</option><option value='Propose for Reschedule'>Propose for Reschedule</option>"
                        } else if (status == 'Rejected') {
                            options = "<option value=" + status + " selected>Rejected</option><option value='Accepted'>Accepted</option><option value=\"Yet to Confirm\">Yet to Confirm</option><option value='Propose for Reschedule'>Propose for Reschedule</option>"
                        } else if (status == 'Propose for Reschedule') {
                            options = "<option value=" + status + " selected>Propose for Reschedule</option><option value=\"Accepted\">Accepted</option><option value=\"Yet to Confirm\">Yet to Confirm</option>"
                        }
                        return "<select id=\"update_status" + id.toString() + "\" name=\"interviewer_acknowledgement\">" + options + "</select>";
                    }
                }

                ],
            });

            // var row_number = '';
            // $('#data tbody').on('click', 'tr', function () {
            //     if ($(this).hasClass('selected')) {
            //         $(this).removeClass('selected');
            //         $("#updatebtn").addClass('disabled');
            //     }
            //     else {
            //         // var rowData = table.rows('.selected').data()[0];
            //         table.$('tr.selected').removeClass('selected');
            //         $(this).addClass('selected');
            //     }
            // });
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
                        // $('#target').attr('action', '/hroffice/interviewer_edit');
                        // $('#target').attr('method', 'post')
                        // $("#target").submit();
                    });

                }
            });

            $('#jobcode').change(function () {
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                var jobcode = $(this).val();
                $.ajax({
                    url: "/hroffice/api/scheduler/shortlistedprofiles/job/" + jobcode,
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
                        $("#candidate").empty();
                        $("#candidate").append("<option value=''>---Select---</option>");

                        // for (var k = 0; k < len; k++) {
                        //     var in_len = dataObj[k]['applicant'].length;
                        //     for (var i = 0; i < in_len; i++) {
                        //         var name = dataObj[k]["applicant"][i]['first_name'] + ' ' + dataObj[k]["applicant"][i]['last_name'];
                        //         var id = dataObj[k]["applicant"][i]['email'];
                        //         $("#candidate").append("<option value='" + id + "'>" + name + "</option>");
                        //     }
                        // }
                        for (var k = 0; k < len; k++) {
                            var name = dataObj[k]["applicant"]['first_name'] + ' ' + dataObj[k]["applicant"]['last_name'];
                            var id = dataObj[k]["applicant"]['email'];
                            $("#candidate").append("<option value='" + id + "'>" + name + "</option>");
                        }

                        console.log(dataObj);
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(errorThrown);
                    }

                });
            });
            var i = 1;
            var interviewer_acknowledgement = ''
            id = '#update_status' + i.toString()
            $('tr').change(function (row_number) {
                interviewer_acknowledgement = $('#update_status' + $(this)[0]['rowIndex']).val();
                // alert(interviewer_acknowledgement);
                //console.log($(this)[0]['cells']);
                //console.log($('#update_status'+$(this)[0]['rowIndex']).val())
                if (interviewer_acknowledgement == 'Propose for Reschedule') {
                    $('#target').attr('action', '/hroffice/interviewer_edit');
                    $('#target').attr('method', 'post');
                    var txn = document.getElementById('txn')
                    txn.value = $(this)[0]['cells'][0]['innerText'] + '#' + $(this)[0]['cells'][2]['innerText'];
                    $("#target").submit();
                }
                if (interviewer_acknowledgement !== 'Propose for Reschedule') {
                    do {
                        var comments = prompt("Please Enter '" + interviewer_acknowledgement + "' status comments!");

                        if (comments == null || comments == "") {
                            var comment = document.getElementById('comment');
                            comment.value = comments;
                        } else {
                            // console.log(table.rows('.selected').data()[0]);
                            var rowData = $(this)[0]['cells'][0]['innerText'];
                            var i_email = $(this)[0]['cells'][4]['innerText'];
                            var c_email = $(this)[0]['cells'][2]['innerText'];
                            var c_name = $(this)[0]['cells'][1]['innerText'];
                            var r_number = $(this)[0]['cells'][5]['innerText'];
                            var sch_date = $(this)[0]['cells'][6]['innerText'];
                            var i_name = $(this)[0]['cells'][3]['innerText'];

                            console.log(rowData, i_email, c_email, comments);
                            var comment = document.getElementById('comment');
                            comment.value = comments;

                            url = "/hroffice/api/scheduler/interviewer_status";

                            $.ajax({
                                "url": url,
                                method: "PUT",
                                data: {
                                    "jobcode": rowData, "i_email": i_email, "interviewer_acknowledgement": interviewer_acknowledgement,
                                    "comment": comments, "c_email": c_email, "c_name": c_name, "r_number": r_number, 'sch_date': sch_date,
                                    "i_name": i_name,
                                },
                                success: function (data, textStatus, jQxhr) {
                                    $('#message').html(data.message);
                                },
                                error: function (jqXhr, textStatus, errorThrown) {
                                    console.log(rowData, interviewer_acknowledgement);
                                    console.log(errorThrown);
                                }
                            }); i++;

                        }
                    } while (comments !== null && comments === "")
                }

            });
            // $('#submit').click(function (e) {
            //     var frm = $('#target')[0];
            //     var frmData = new FormData(frm)
            //     $.ajax({
            //         url: "/hroffice/api/scheduler/addrecord",
            //         type: 'POST',
            //         cache: false,
            //         processData: false,
            //         contentType: false,
            //         timeout: 600000,
            //         data: frmData,
            //         success: function (data, textStatus, jQxhr) {
            //             $('#message').html(data.message);
            //             console.log(data);
            //         },
            //         error: function (jqXhr, textStatus, errorThrown) {
            //             console.log(errorThrown);
            //         }
            //     });
            // });

            $(document).ready(function () {
                $('#updsubmit').click(function (e) {
                    $("#target").validate();
                    if (!$("#target").valid()) {
                        return false;
                    }
                    var frm = $('#target')[0];
                    var frmData = new FormData(frm);

                    $.ajax({
                        url: "/hroffice/api/scheduler/interviewer_edit",
                        type: 'PUT',
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
            });

            // var row_number = '';
            // $('#data tbody').on('click', 'tr', function () {
            //     if ($(this).hasClass('selected')) {
            //         $(this).removeClass('selected');
            //         $("#updatebtn").addClass('disabled');
            //     }
            //     else {

            //         table.$('tr.selected').removeClass('selected');
            //         $(this).addClass('selected');
            //         console.log(table.rows('.selected').data()[0]['interviewer_email']);
            //         selected_value = table.rows('.selected').data()[0]['interviewer_email'];
            //         var dataset = selected_value;
            //         var txn = document.getElementById('txn');
            //         txn.value = dataset;
            //         $(this).closest("tr");
            //         var tr = $(this).closest("tr");
            //         var row_number = tr.index();
            //         //alert(row_number);
            //         $("#updatebtn").removeClass('disabled');
            //         $('#updatebtn').click(function () {
            //             var txn = document.getElementById('txn');
            //             alert(table.rows('.selected').data()[0]);
            //             selected_value = table.rows('.selected').data()[0]['interviewer_email'];
            //             var dataset = selected_value;
            //             txn.value = dataset;
            //             $('#target').attr('action', '/hroffice/editschedule');
            //             $('#target').attr('method', 'post');
            //             $("#target").submit();
            //         });
            //     }
            // });



            // =================================================================================================
        },
        loadData: function (successCallback) {
            url = '/hroffice/api/scheduler/getrecords';
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
        SchedulerProfile.loadData(SchedulerProfile.populateDataTable);
    });
})();

