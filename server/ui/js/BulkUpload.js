$('#target').ready(function () {
    $('#loading').hide();
    $('#submit').click(function (e) {
        $("#target").validate();
        if (!$("#target").valid()) {
            return false;
        }
        var frm = $('#target')[0];
        var frmData = new FormData(frm)
        $.ajax({
            url: '/hroffice/api/applications/upload-bulk-applications',
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
                $('#message').html(data.message + ' &nbsp; this page Redirecting soon.... in 5 seconds!!!');
                console.log('Thank God it worked!');
                var delay = 5000;
                var url = "/hroffice/applications/candidateprofile"
                setTimeout(function () { window.location = url; }, delay);
            },
            error: function (jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    });
});