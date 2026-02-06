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


    let educationProfile = {
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
                "columns": [{ "data": "qualification" }, { "data": "specialisation" }, { "data": "university" }, { "data": "qualification_description" },
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


            $(document).ready(function () {
                $('#submit').click(function (e) {
                    $('#target').validate();
                    if (!$('#target').valid()) {
                        return false;
                    }
                    var frm = $('#target')[0];
                    var frmData = new FormData(frm)
                    $.ajax({
                        url: "/hroffice/api/educations/addrecord",
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
            });


            $(document).ready(function () {
                $('#updsubmit').click(function (e) {
                    e.preventDefault();
                    $("#target").validate();
                    if (!$("#target").valid()) {
                        return false;
                    }
                    var frm = $('#target')[0];
                    var frmData = new FormData(frm)
                    $.ajax({
                        url: "/hroffice/api/educations/putrecord",
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
                    console.log(table.rows('.selected').data()[0]['qualification']);
                    selected_value = table.rows('.selected').data()[0]['qualification'];
                    specialisation_value = table.rows('.selected').data()[0]['specialisation'];
                    status = table.rows('.selected').data()[0]['status'];
                    txn = table.rows('.selected').data()[0]['qualification'];
                    var txn = document.getElementById('txn')
                    txn.value = selected_value + '#' + specialisation_value;
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
                        selected_value = table.rows('.selected').data()[0]['qualification']
                        specialisation_value = table.rows('.selected').data()[0]['specialisation'];

                        var txn = document.getElementById('txn')
                        txn.value = selected_value + '#' + specialisation_value;
                        $('#target').attr('action', '/hroffice/editeducation');
                        $('#target').attr('method', 'post');
                        $("#target").submit();
                    });
                }
            });
            var i = 0;
            $('#update_status').click(function (row_number) {
                var rowData = table.rows('.selected').data()[0]['qualification'];
                specialisation_value = table.rows('.selected').data()[0]['specialisation'];

                var status = table.rows('.selected').data()[0]['status'];
                if ($('#update_status').text() == "Mark Disable") {
                    status = 'false';
                } else if ($('#update_status').text() == "Mark Enable") {
                    status = 'true';
                }

                url = "/hroffice/api/educations/editstatus";
                $.ajax({
                    "url": url,
                    method: 'PUT',
                    data: { "qualification": rowData, "status": status, 'specialisation': specialisation_value },
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


            // $('#deletedata').click(function () {
            //     if (confirm("Are you sure you want to delete the selected rows?")) {
            //         var rowData = table.rows('.selected').data()['code'];
            //         url = "/hroffice/api/jobs/deleterecord/code/" + rowData
            //         $.ajax({
            //             "url": url,
            //             method: 'DELETE',
            //             contentType: 'application/json',
            //             success: function (data, textStatus, jQxhr) {
            //                 $('#message').html(data.message);
            //                 console.log(data);
            //                 table.row('.selected').remove().draw(false);
            //             },
            //             error: function (jqXhr, textStatus, errorThrown) {
            //                 console.log(errorThrown);
            //             }
            //         });
            //     }
            // });
        },
        loadData: function (successCallback) {
            url = '/hroffice/api/educations/fetchrecord'
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
        educationProfile.loadData(educationProfile.populateDataTable);
    });
})();

