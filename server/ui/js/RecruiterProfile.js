(function () {
    var $loading = $('#loading').hide();

    let RecruiterProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            // clear the table before populating it with more data
            //$("#data").DataTable().clear();
            console.log("populating data table...");
            //  var result = "";
            //  var i = 1;
            // for (var key in data) {
            //     alert(data[key].code)
            //     result += i + ". " + key + ": " + data[key].name + " ";
            // //   var customer = data.customers['job'+i];
            //     console.log(result)
            //    i++;
            // } //key in question is the index of the array 0, 1,
            $.fn.dataTable.ext.errMode = 'none';
            $('#data').on('error.dt', function (e, settings, techNote, message) {
                console.log('An error has been reported by DataTables: ', message);
            });
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "emp_id" }, { "data": "name" }, { "data": "phone" },
                { "data": "email" }, { "data": "location" },
                {
                    "data": "status",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        status = row.status;
                        if (status == 'true') {
                            status = 'Enable';
                        } else {
                            status = 'Disable';
                        }
                        return '<span id="status"  >' + status + '</span>';
                    },
                }
                ],
            });
            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    $('#update_status').text('Enable/Disable');
                    $("#updatebtn").addClass('disabled');
                    $("#update_status").addClass('disabled');

                }
                else {
                    //var rowData = table.rows('.selected').data()[0]['code'];
                    //console.log(rowData);
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    console.log(table.rows('.selected').data()[0]['emp_id'])
                    selected_value = table.rows('.selected').data()[0]['emp_id']
                    $("#updatebtn").removeClass('disabled');
                    $("#update_status").removeClass('disabled');

                    status = table.rows('.selected').data()[0]['status'];

                    if (status === undefined || status == 'true') {
                        $('#update_status').text('Mark Disable');
                    } else {
                        $('#update_status').text('Mark Enable');
                    }
                    $('#updatebtn').click(function () {
                        selected_value = table.rows('.selected').data()[0]['emp_id']
                        var txn = document.getElementById('txn')
                        txn.value = selected_value;
                        $('#target').attr('action', '/hroffice/editrecruiter');
                        $('#target').attr('method', 'post')
                        $("#target").submit();
                    });
                }
            });

            var i = 0;
            $('#update_status').click(function (row_number) {
                var rowData = table.rows('.selected').data()[0]['emp_id'];
                var status = table.rows('.selected').data()[0]['status'];
                if ($('#update_status').text() == "Mark Disable" && i !== 0) {
                    status = 'false';
                } else if ($('#update_status').text() == "Mark Enable" && i !== 0) {
                    status = 'true';
                }
                url = "/hroffice/api/recruiter/editstatus";
                $.ajax({
                    "url": url,
                    method: 'PUT',
                    data: { "emp_id": rowData, "status": status, },
                    beforeSend: function () {
                        $('#loading').show();
                    },
                    complete: function () {
                        $('#loading').hide();
                    },
                    success: function (data, textStatus, jQxhr) {
                        $('#message').html(data.message);
                        console.log(data);
                        if ($('#update_status').text() == "Mark Disable") {
                            // table.rows('.selected').data()[0]['status']= 'Disable';
                            $('#update_status').text("Mark Enable");
                            $('table > tbody > tr.selected > td:last').text('Disable');
                        } else {
                            //table.rows('.selected').data()[0]['status']= 'Enable';
                            //alert(String($('#update_status').text('Mark Enable')));
                            $('#update_status').text("Mark Disable");
                            $('table > tbody > tr.selected > td:last').text('Enable');
                        }
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(errorThrown);
                    }
                });
                i++;
            });

            $('#deletedata').click(function () {

                if (confirm("Are you sure you want to delete the selected rows?")) {
                    var rowData = table.rows('.selected').data()['code'];
                    url = "/hroffice/api/jobs/deleterecord/code/" + rowData
                    $.ajax({
                        "url": url,
                        method: 'DELETE',
                        contentType: 'application/json',
                        beforeSend: function () {
                            $('#loading').show();
                        },
                        complete: function () {
                            $('#loading').hide();
                        },
                        success: function (data, textStatus, jQxhr) {
                            $('#message').html(data.message);
                            console.log(data);
                            table.row('.selected').remove().draw(false);

                        },
                        error: function (jqXhr, textStatus, errorThrown) {
                            console.log(errorThrown);
                        }
                    });
                }
            });

            $('#submit').click(function (e) {
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: '/hroffice/api/recruiter/addrecord',
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
                })
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
                        url: '/hroffice/api/recruiter/putrecord',
                        type: 'PUT',
                        cache: false,
                        processData: false,
                        contentType: false,
                        timeout: 60000,
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
                    })
                });
            });

            $('#updatefillform').click(function () {

                var rowData = table.rows('.selected').data()[0]['code'];
                document.getElementById("txn").value = rowData
                window.location.href = "RecruiterProfile_update.html"
                url = '/hroffice/api/recruiter/getrecords'
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
                        if (true) {
                            $("#emp_id").val(myJsonData['emp_id']);
                            $("#first_name").val(myJsonData['first_name']);
                            $("#last_name").val(myJsonData['last_name']);
                            $("#phone").val(myJsonData['phone']);
                            $("#email").val(myJsonData['email']);
                            $("#location").val(myJsonData['location']);
                            $("#status").val(myJsonData['status']);

                        }
                    }
                });
                // url = "localhost:8000/hroffice/api/jobs/updaterecord/code/" + rowData
                // $.ajax({
                //     "url": url,
                //     method: 'PUT',
                //     contentType: 'application/json',
                //     success: function (data, textStatus, jQxhr) {
                //         $('#message').html(data.message);
                //         console.log(data);
                //         table.row('.selected').remove().draw(false);
                //     },
                //     error: function (jqXhr, textStatus, errorThrown) {
                //         console.log(errorThrown);
                //     }
                // });
            });
        },
        loadData: function (successCallback) {
            url = '/hroffice/api/recruiter/getrecords'
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
                    console.log(data);
                    successCallback(myJsonData);
                },
                error: function (e) {
                    console.log("There was an error with your request...");
                    console.log("error: " + JSON.stringify(e));
                }
            });
        }
    };
    $('target').ready(function () {
        $.noConflict();
        RecruiterProfile.loadData(RecruiterProfile.populateDataTable);
    });
})();

