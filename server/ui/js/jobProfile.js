$.getScript('https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js', function () {
    // script is now loaded and executed.
    // put your dependent JS here.
});
(function () {
    let jobProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            $.fn.dataTable.ext.errMode = 'none';
            $('#data').on('error.dt', function (e, settings, techNote, message) {
                console.log('An error has been reported by DataTables: ', message);
            });
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "code" }, { "data": "title" }, { "data": "positions" }, { "data": "experience" },
                { "data": "hr_name" }, { "data": "hr_name" }, { "data": "client" },
                { "data": "location" },
                {
                    "data": "code",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/jobpreviewfile?code=' + row.code + '">View</a></span>';
                    }
                },
                {
                    "data": "job_status",
                    "sWidth": "5%",
                    "mRender": function (data, type, row, meta) {
                        status = row.job_status;
                        options = ""
                        id = meta.row + meta.settings._iDisplayStart + 1;
                        if (status == "Open") {
                            options = "<option value=" + status + " selected>" + status + "</option><option value=\"Active\">Active</option><option value='Hold'>Hold</option><option value=\"Closed\">Closed</option><option value='Filled'>Filled</option>"
                        } else if (status == 'Active') {
                            options = "<option value=" + status + " selected>Active</option><option value=\"Open\">Open</option><option value='Hold'>Hold</option><option value=\"Closed\">Closed</option><option value='Filled'>Filled</option>"
                        } else if (status == 'Hold') {
                            options = "<option value=" + status + " selected>Hold</option><option value=\"Open\">Open</option><option value='Active'>Active</option><option value=\"Closed\">Closed</option><option value='Filled'>Filled</option>"
                        } else if (status == 'Closed') {
                            options = "<option value=" + status + " selected>Closed</option><option value=\"Open\">Open</option><option value='Hold'>Hold</option><option value=\"Active\">Active</option><option value='Filled'>Filled</option>"
                        } else if (status == 'Filled') {
                            options = "<option value=" + status + " selected>Filled</option><option value=\"Open\">Open</option><option value='Hold'>Hold</option><option value=\"Closed\">Closed</option><option value='Active'>Active</option>"
                        }
                        return "<select id=\"update_status" + id.toString() + "\" name=\"job_status\">" + options + "</select>";
                    }
                }
                ],
            });
            var row_number = '';
            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    $('#update_status').text('Enable/Disable');
                    $("#updatebtn").addClass('disabled');
                    $("#update_status").addClass('disabled');
                }
                else {

                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    console.log(table.rows('.selected').data()[0]['code']);
                    selected_value = table.rows('.selected').data()[0]['code'];
                    status = table.rows('.selected').data()[0]['status'];
                    txn = table.rows('.selected').data()[0]['code'];
                    var txn = document.getElementById('txn')
                    txn.value = selected_value;
                    $(this).closest("tr");
                    var tr = $(this).closest("tr");
                    var row_number = tr.index();
                    //alert(row_number);
                    $("#updatebtn").removeClass('disabled');
                    $("#update_status").removeClass('disabled');

                    if (status === undefined || status == 'true') {
                        $('#update_status').text('Mark Disable');
                    } else {
                        $('#update_status').text('Mark Enable');
                    }
                    $('#updatebtn').click(function () {
                        selected_value = table.rows('.selected').data()[0]['code']
                        var txn = document.getElementById('txn')
                        txn.value = selected_value;
                        $('#target').attr('action', '/hroffice/editjobprofile');
                        $('#target').attr('method', 'post');
                        $("#target").submit();
                    });
                }
            });

            var i = 1;
            var job_status = ''
            id = '#update_status' + i.toString()
            $('tr').change(function (row_number) {
                job_status = $('#update_status' + $(this)[0]['rowIndex']).val();
                var rowData = $(this)[0]['cells'][0]['innerText'];

                console.log(rowData, job_status);
                url = "/hroffice/api/jobs/updatestatus";
                $.ajax({
                    "url": url,
                    method: "PUT",
                    data: { "code": rowData, "job_status": job_status },
                    success: function (data, textStatus, jQxhr) {
                        $('#message').html(data.message);
                    },
                    error: function (jqXhr, textStatus, errorThrown) {
                        console.log(rowData, job_status);
                        console.log(errorThrown);
                    }
                }); i++;
            });

            $('#submit').click(function (e) {
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: '/hroffice/api/jobs/addrecord',
                    type: 'POST',
                    enctype: 'multipart/form-data',
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

            $('#updsubmit').click(function (e) {
                e.preventDefault();
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                $.ajax({
                    url: '/hroffice/api/jobs/updaterecord',
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


            $('#updatefillform').click(function () {

                var rowData = table.rows('.selected').data()[0]['code'];
                document.getElementById("txn").value = rowData
                window.location.href = "jobprofile_update.html"
                url = '/hroffice/api/jobs/getrecords'
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
                            $("#code").val(myJsonData['code']);
                            $("#title").val(myJsonData['title']);
                            $("#location").val(myJsonData['location']);
                            $("#desc").val(myJsonData['desc']);
                            $("#positions").val(myJsonData['positions']);
                            $("#experience").val(myJsonData['experience']);
                            $("#edu").val(myJsonData['edu']);
                            $("#interview_pattern").val(myJsonData['interview_pattern']);
                            $("#client").val(myJsonData['client']);
                        }
                    }
                });
            });
        },
        loadData: function (successCallback) {
            url = '/hroffice/api/jobs/getrecords'
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
                    //jobcode = document.getElementById('filter').value;
                    //$('input[type=search]').val(jobcode);
                    // if (jobcode != 'None') {
                    //     $('input[type=search]').val('');
                    //     $("input[type=search]").focus().select();
                    // }
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
        jobProfile.loadData(jobProfile.populateDataTable);

    });
})();

