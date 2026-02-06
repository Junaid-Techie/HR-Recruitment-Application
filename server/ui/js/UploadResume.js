(function () {
    var $loading = $('#loading').hide();
    let CandidateProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            // clear the table before populating it with more data
            //$("#data").DataTable().clear();
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
                "columns": [
                    { "data": "code" },
                    {
                        data: null, render: function (data, type, row) {
                            // Combine the first and last names into a single table field
                            if (data.last_name === undefined || data.last_name === 'undefined') {
                                return data.first_name;
                            } else {
                                return data.first_name + ' ' + data.last_name;
                            }
                        }
                    },
                    { "data": "experience" },
                    { "data": "phone" },
                    { "data": "email" }, { "data": "primary_skill", },
                    {
                        "data": "code",
                        "sWidth": "5%",
                        "mRender": function (data, type, row) {
                            return '<span id="job" > <a href="/hroffice/api/applications/candidatepreviewfile?code=' + row.code + '&email=' + row.email + '">View</a></span>';
                        }
                    },
                    { "data": "notice_period", },
                    {
                        "data": "status",
                        "sWidth": "5%",
                        "mRender": function (data, type, row) {
                            status = row.status;
                            if (status == 'null' || status == 'true' || status == 'undefined' || status === undefined || status === '') {
                                status = 'Enable';
                            } else {
                                status = 'Disable';
                            }
                            return '<span id="status"  >' + status + '</span>';
                        }
                    }
                ],
                responsive: true,
            });

            $('#submit').click(function (e) {
                $("#target").validate();
                if (!$("#target").valid()) {
                    return false;
                }
                var frm = $('#target')[0];
                var frmData = new FormData(frm)
                $.ajax({
                    url: '/hroffice/api/applications/upload-applications',
                    type: 'POST',
                    cache: false,
                    processData: false,
                    contentType: false,
                    enctype: 'multipart/form-data',
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
                var frmData = new FormData(frm)
                $.ajax({
                    url: '/hroffice/api/applications/putrecord',
                    type: 'PUT',
                    cache: false,
                    processData: false,
                    contentType: false,
                    enctype: 'multipart/form-data',
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


            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    $("#updatebtn").addClass('disabled');
                    $("#update_status").addClass('disabled');
                }
                else {
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');
                    selected_value = table.rows('.selected').data()[0]['code']
                    $("#updatebtn").removeClass('disabled');
                    $("#update_status").removeClass('disabled');
                    status = table.rows('.selected').data()[0]['status'];
                    if (status === undefined || status == 'true') {
                        $('#update_status').text('Mark Disable');
                    } else {
                        $('#update_status').text('Mark Enable');
                    }

                    $('#updatebtn').click(function () {
                        selected_value = table.rows('.selected').data()[0]['code'];
                        phone_value = table.rows('.selected').data()[0]['phone'];
                        var txn = document.getElementById('txn')
                        txn.value = selected_value + '#' + phone_value;
                        $('#target').attr('action', '/hroffice/applications/editcandidate');
                        $('#target').attr('method', 'post');
                        $("#target").submit();
                    });


                    var i = 0;
                    $('#update_status').click(function (row_number) {
                        var rowData = table.rows('.selected').data()[0]['code'];
                        var phone = table.rows('.selected').data()[0]['phone'];
                        if ($('#update_status').text() == "Mark Disable" && i !== 0) {
                            status = 'false';
                        } else if ($('#update_status').text() == "Mark Enable" && i !== 0) {
                            status = 'true';
                        }
                        url = "/hroffice/api/applications/editcandidate_status";
                        $.ajax({
                            "url": url,
                            method: 'PUT',
                            data: { "txn": rowData + '#' + phone, "status": status, },
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
                }
            });
        },

        loadData: function (successCallback) {
            url = '/hroffice/api/applications'
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
        CandidateProfile.loadData(CandidateProfile.populateDataTable);
    });
})();

