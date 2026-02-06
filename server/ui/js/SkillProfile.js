// $.getScript('https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js', function () {
//     // script is now loaded and executed.
//     // put your dependent JS here.
// });
(function () {
    let skillProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "skill_name" }, { "data": "skill_desc" },
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
                    //var rowData = table.rows('.selected').data()[0]['code'];
                    //console.log(rowData);
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    console.log(table.rows('.selected').data()[0]['skill_name']);
                    selected_value = table.rows('.selected').data()[0]['skill_name'];
                    status = table.rows('.selected').data()[0]['status'];
                    $(this).closest("tr");
                    var tr = $(this).closest("tr");
                    var row_number = tr.index();
                    $("#updatebtn").removeClass('disabled');
                    $("#update_status").removeClass('disabled');

                    //alert(row_number);
                    if (status === undefined || status == 'true') {

                        $('#update_status').text('Mark Disable');

                    } else {
                        $('#update_status').text('Mark Enable');
                    }
                    $('#updatebtn').click(function () {
                        selected_value = table.rows('.selected').data()[0]['skill_name'];
                        var txn = document.getElementById('txn');
                        txn.value = selected_value;
                        $('#target').attr('action', '/hroffice/editskill');
                        $('#target').attr('method', 'post');
                        $("#target").submit();
                    });
                }
            });
            $('#submit').click(function (e) {
                $('#target').validate();
                if (!$('#target').valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: '/hroffice/api/skills/addskill',
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

            $('#updsubmit').click(function (e) {
                e.preventDefault();
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm);
                $.ajax({
                    url: "/hroffice/api/skills/editrecord",
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

            var i = 0;
            $('#update_status').click(function (row_number) {
                var rowData = table.rows('.selected').data()[0]['skill_name'];
                var status = table.rows('.selected').data()[0]['status'];
                if ($('#update_status').text() == "Mark Disable" && i !== 0) {
                    status = 'false';
                } else if ($('#update_status').text() == "Mark Enable" && i !== 0) {
                    status = 'true';
                }

                url = "/hroffice/api/skills/editstatus";
                $.ajax({
                    "url": url,
                    method: 'PUT',
                    data: { "skill_name": rowData, "status": status, },
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
        },
        loadData: function (successCallback) {
            url = 'http://localhost:8000/hroffice/api/skills/fetchskills'
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

    $('target').ready(function () {
        $.noConflict();
        skillProfile.loadData(skillProfile.populateDataTable);
    });

})();

