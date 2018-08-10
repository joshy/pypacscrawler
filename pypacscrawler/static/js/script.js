$(function () {
    console.log('ready');

    $('#upload-button').on('click', function (e) {
        e.preventDefault();
        var acc = $('#search-input').val();
        var data = {
          'acc': acc
        }
        $.ajax({
          type: 'POST',
          url: 'upload',
          data: JSON.stringify(data),
          dataType: 'json'
        }).done(function (data) {
          noty({
            text: 'Successfully uploaded to RIS/PACS Crawler',
            layout: 'centerRight',
            timeout: '3000',
            closeWith: ['click', 'hover'],
            type: 'success'
          });
        }).fail(function (error) {
          noty({
            text: 'Upload failed: ' + error.responseText,
            layout: 'topRight',
            timeout: '3000',
            closeWith: ['click', 'hover'],
            type: 'error'
          });
          console.log(error);
          console.error("Upload failed");
        });
      });
});