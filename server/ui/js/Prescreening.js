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

    let PrescreenProfile = {
        populateDataTable: function (data) {
            console.log("populating data table...", data);
            console.log("populating data table...");
            var selected_value = ''
            var table = $('#data').DataTable({
                "data": data,
                "columns": [{ "data": "jobcode", "sWidth": "5%" }, { "data": "candidate_name", "sWidth": "5%" }, { "data": "candidate_email", "sWidth": "5%" },
                { "data": "candidate_phone", "sWidth": "5%" }, { "data": "candidate_primary_skill", "sWidth": "20%" },

                {
                    "data": "jobcode",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/jobpreviewfile?code=' + row.jobcode + '">View</a></span>';
                    }
                },
                {
                    "data": "jobcode",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/candidatepreviewfile?code=' + row.jobcode + '&email=' + row.candidate_email + '">View</a></span>';
                    }
                },

                {
                    "data": "candidate_prescreen_status",
                    "sWidth": "5%",
                    "mRender": function (data, type, row, meta) {
                        status = row.candidate_prescreen_status;
                        options = ""
                        id = meta.row + meta.settings._iDisplayStart + 1;
                        if (status == 'New') {
                            options = "<option value=" + status + " selected>" + status + "</option><option value='Accept'>Accept</option><option value='Hold'>Hold</option><option value='Reject'>Reject</option>"
                        } else if (status == 'Accept') {
                            options = "<option value=" + status + " selected>Accept</option><option value='Hold'>Hold</option><option value='New'>New</option><option value='Reject'>Reject</option>"
                        } else if (status == 'Reject') {
                            options = "<option value=" + status + " selected>Reject</option><option value='Accept'>Accept</option><option value='Hold'>Hold</option><option value='New'>New</option>"
                        } else {
                            options = "<option value=" + status + " selected>Hold</option><option value='Accept'>Accept</option><option value='New'>New</option><option value='Reject'>Reject</option>"
                        }
                        return '<select id="update_status' + id.toString() + '"name="shortlist_status">' + options + '</select>';
                    }
                }

                ],
            });

            var row_number = '';
            $('#data tbody').on('click', 'tr', function () {
                if ($(this).hasClass('selected')) {
                    $(this).removeClass('selected');
                    //$('#update_status').text('Accept/Reject');
                    $("#updatebtn").addClass('disabled');
                    //$("#update_status").addClass('disabled');
                }
                else {
                    //var rowData = table.rows('.selected').data()[0]['code'];
                    //console.log(rowData);
                    table.$('tr.selected').removeClass('selected');
                    $(this).addClass('selected');

                }
            });
            var i = 1;
            var shortlist_status = ''
            id = '#update_status' + i.toString()
            $('tr').change(function (row_number) {
                shortlist_status = $('#update_status' + $(this)[0]['rowIndex']).val();
                //console.log($(this)[0]['cells']);
                //console.log($('#update_status'+$(this)[0]['rowIndex']).val())
                do {
                    var comments = prompt("Please Enter " + shortlist_status + " status comments!");

                    if (comments == null || comments == "") {
                        var comment = document.getElementById('comment');
                        comment.value = comments;
                    } else {
                        console.log(table.rows('.selected').data()[0]);
                        var rowData = $(this)[0]['cells'][0]['innerText'];
                        var c_email = $(this)[0]['cells'][2]['innerText'];
                        var c_phone = $(this)[0]['cells'][3]['innerText'];
                        var c_name = $(this)[0]['cells'][1]['innerText'];
                        console.log(rowData, c_email, c_phone, c_name);
                        var comment = document.getElementById('comment');
                        comment.value = comments;
                        url = "/hroffice/api/prescreen/editstatus";

                        $.ajax({
                            "url": url,
                            method: "PUT",
                            data: { "jobcode": rowData, "c_email": c_email, "c_phone": c_phone, "shortlist_status": shortlist_status, "comment": comments, "c_name": c_name },
                            beforeSend: function () {
                                $('#loading').show();
                            },
                            complete: function () {
                                $('#loading').hide();
                            },
                            success: function (data, textStatus, jQxhr) {
                                $('#message').html(data.message);
                            },
                            error: function (jqXhr, textStatus, errorThrown) {
                                console.log(rowData, shortlist_status);
                                console.log(errorThrown);
                            }
                        }); i++;

                    }
                } while (comments !== null && comments === "")


            });



        },
        loadData: function (successCallback) {
            url = '/hroffice/api/prescreen/getrecords';
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
        PrescreenProfile.loadData(PrescreenProfile.populateDataTable);
    });
})();

