

(function () {


    let SchedulerProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "jobcode" }, { "data": "candidate_name" }, { "data": "candidate_email" },
                { "data": "interviewer_name" }, { "data": "interviewer_email" }, { "data": "scheduled_datetime" },
                {
                    "data": "interviewer_acknowledgement",
                    "sWidth": "5%",
                    "mRender": function (data, type, row, meta) {
                        status = row.interviewer_acknowledgement;
                        options = ""
                        id = meta.row + meta.settings._iDisplayStart + 1;
                        if (status == 'Yet to Confirm') {
                            options = "<option value=" + status + " selected>" + status + "</option><option value='Accepted'>Accepted</option><option value='Rejected'>Rejected</option>"
                        } else if (status == 'Accepted') {
                            options = "<option value=" + status + " selected>Accepted</option><option value='Rejected'>Rejected</option><option value='Yet to Confirm'>Yet to Confirm</option>"
                        } else {
                            options = "<option value=" + status + " selected>Rejected</option><option value='Accepted'>Accepted</option><option value='Yet to Confirm'>Yet to Confirm</option>"
                        }
                        return '<select id="update_status' + id.toString() + '"name="interviewer_acknowledgement">' + options + '</select>';
                    }
                }

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
                        $('#target').attr('action', '/hroffice/interviewer_update');
                        $('#target').attr('method', 'post')
                        $("#target").submit();
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
            var interviewer_acknowledgement = ''
            id = '#update_status' + i.toString()
            $('tr').change(function (row_number) {
                interviewer_acknowledgement = $('#update_status' + $(this)[0]['rowIndex']).val();
                //console.log($(this)[0]['cells']);
                //console.log($('#update_status'+$(this)[0]['rowIndex']).val())
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

                        console.log(rowData, i_email, c_email, comments);
                        var comment = document.getElementById('comment');
                        comment.value = comments;

                        url = "/hroffice/api/scheduler/interviewer_status";

                        $.ajax({
                            "url": url,
                            method: "PUT",
                            data: {
                                "jobcode": rowData, "i_email": i_email, "interviewer_acknowledgement": interviewer_acknowledgement,
                                "comment": comments, "c_email": c_email, "c_name": c_name,
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
                        url: "/hroffice/api/scheduler/reschedule",
                        type: 'PUT',
                        cache: false,
                        processData: false,
                        contentType: false,
                        timeout: 600000,
                        data: frmData,
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
            url = '/hroffice/api/scheduler/notschedule';
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

