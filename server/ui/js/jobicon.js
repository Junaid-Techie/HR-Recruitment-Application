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
                "columns": [{ "data": "code" }, { "data": "title" }, { "data": "desc" }, { "data": "positions" }, { "data": "experience" },
                { "data": "edu" }, { "data": "interview_pattern" }, { "data": "client" }, { "data": "location" },
                {
                    "data": "code",
                    "sWidth": "5%",
                    "mRender": function (data, type, row) {
                        return '<span id="job" > <a href="/hroffice/api/applications/jobpreviewfile?code=' + row.code + '">View</a></span>';
                    }
                },
                { "data": "job_status" },
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

        },
        loadData: function (successCallback) {
            url = '/hroffice/api/jobs/getnotclosed'
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
                    jobcode = document.getElementById('filter').value;
                    $('input[type=search]').val(jobcode);
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

