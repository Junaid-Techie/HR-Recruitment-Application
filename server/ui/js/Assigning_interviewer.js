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
                "columns": [{ "data": "job" }, { "data": "candidate" }, { "data": "candidate_email" }, { "data": "interviewer_name" }, { "data": "interviewer_email" },
                { "data": "interview_type" }, { "data": "scheduled_datetime" },
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
                { "data": "interviewer_acknowledgement" },

                {
                    // 'Yet to confirm', 'Accepted', 'Rejected', 'Reschedule'
                    "data": "schedule_status",
                    "mRender": function (data, type, row, meta) {
                        status = row.schedule_status;
                        options = ""
                        id = meta.row + meta.settings._iDisplayStart + 1;
                        if (status == "Yet to Confirm") {
                            options = "<option value=" + status + " selected>" + status + "</option><option value=\"Reschedule\">Reschedule</option><option value='Ready'>Ready</option>"
                        } else if (status == 'Ready') {
                            options = "<option value=" + status + " selected>Ready</option><option value=\"Yet to Confirm\">Yet to Confirm</option></option><option value=\"Reschedule\">Reschedule</option><option value='Reschedule>Reschedule</option>"
                        }
                        return '<select id="update_status' + id.toString() + '"name="schedule_status">' + options + '</select>';
                    }
                },
                ],
            });

            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    schedule_status = $('#update_status' + $(this)[0]['rowIndex']).val();
                    if (schedule_status !== 'Reschedule') {
                        $("#updatebtn").addClass('disabled');
                    } else {
                        $("#updatebtn").removeClass('disabled');
                    }
                }
                else {
                    //var rowData = table.rows('.selected').data()[0]['code'];
                    //console.log(rowData);
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    console.log(table.rows('.selected').data()[0]['candidate_email'])
                    selected_value = table.rows('.selected').data()[0]['job']
                    var txn = document.getElementById('txn');
                    candidate_value = table.rows('.selected').data()[0]['candidate_email']
                    txn.value = selected_value + '#' + candidate_value;
                }
            });
            // $('#updatebtn').click(function () {
            //     $('#target').attr('action', '/hroffice/editinterviewer');
            //     $('#target').attr('method', 'post');
            //     $("#target").submit();
            // });
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
            var schedule_status = ''
            id = '#update_status' + i.toString()
            $('tr').change(function (row_number) {
                schedule_status = $('#update_status' + $(this)[0]['rowIndex']).val();
                //console.log($(this)[0]['cells']);
                //console.log($('#update_status'+$(this)[0]['rowIndex']).val())
                if (schedule_status == 'Reschedule') {
                    $('#target').attr('action', '/hroffice/editinterviewer');
                    $('#target').attr('method', 'post');
                    $("#target").submit();
                }
                if (schedule_status !== 'Reschedule') {
                    do {
                        var comments = prompt("Please Enter '" + schedule_status + "' status comments!");

                        if (comments == null || comments == "") {
                            var comment = document.getElementById('comment');
                            comment.value = comments;
                        } else {
                            // console.log(table.rows('.selected').data()[0]);
                            var rowData = $(this)[0]['cells'][0]['innerText'];
                            var c_name = $(this)[0]['cells'][1]['innerText'];
                            var c_email = $(this)[0]['cells'][2]['innerText'];
                            var i_email = $(this)[0]['cells'][4]['innerText'];
                            var i_type = $(this)[0]['cells'][5]['innerText'];
                            var i_name = $(this)[0]['cells'][3]['innerText'];
                            var sch_date = $(this)[0]['cells'][6]['innerText'];

                            console.log(rowData, i_email, c_email, comments);
                            var comment = document.getElementById('comment');
                            comment.value = comments;

                            url = "/hroffice/api/scheduler/recruiter_status";

                            $.ajax({
                                "url": url,
                                method: "PUT",
                                data: {
                                    "jobcode": rowData, "i_email": i_email, "schedule_status": schedule_status, "comment": comments,
                                    "c_email": c_email, "c_name": c_name, "i_type": i_type, 'i_name': i_name, 'sch_date': sch_date
                                },
                                success: function (data, textStatus, jQxhr) {
                                    $('#message').html(data.message);
                                },
                                error: function (jqXhr, textStatus, errorThrown) {
                                    console.log(rowData, schedule_status);
                                    console.log(errorThrown);
                                }
                            }); i++;
                        }
                    } while (comments !== null && comments === "")
                }
            });
            $('#submit').click(function (e) {
                e.preventDefault();
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: "/hroffice/api/scheduler/assign_interviewer",
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

            $(document).ready(function () {
                $('#updsubmit').click(function (e) {
                    e.preventDefault();
                    $("#target").validate();
                    if (!$("#target").valid()) {
                        return false;
                    }
                    var frm = $('#target')[0];
                    var frmData = new FormData(frm);

                    $.ajax({
                        url: "/hroffice/api/scheduler/re_assign",
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

