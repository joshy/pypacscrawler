$(function () {
  console.log('ready');

  $('#batch-upload').submit(function (e) {
    var form = $(this);
    var url = form.attr('action');

    $.ajax({
      type: "GET",
      url: url,
      data: form.serialize(),
      success: function (data) {
        console.log(data);
        new Noty({
          theme: 'sunset',
          type: 'info',
          text: 'Jobs submitted'
        }).show();
      }
    })
    e.preventDefault();
  });


  $('#upload-button').on('click', function (e) {
    e.preventDefault();
    var acc = $('#search-input').val();
    var day = $('#day-input').val();
    var data = {
      'acc': acc,
      'day': day
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