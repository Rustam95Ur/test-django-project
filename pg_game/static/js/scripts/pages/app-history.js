/****************************************************************
 *               Limit File Size and No. Of Files                *
 ****************************************************************/
var file_object = '';
Dropzone.autoDiscover = false;
var success_btn = $('#save_file_btn')
$("#upload_save_file").dropzone({
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 0.5, // MB
    maxFiles: 1,
    url: '/file_upload',
    init: function () {
        var submitButton = document.querySelector("[type=submit]");
        submitButton.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            let xhr = new XMLHttpRequest();
            xhr.open('POST', '/file_save', true);
            xhr.onload = xhr.onerror = function () {
                if(xhr.status === 500) {
                    console.log(this.response)
                    var title = 'Ошибка при сохранений!'
                    var message = 'Пожалуйста, попробуйте еще раз. Либо обратитесь к администратору'
                    var status = 'error'
                } else {
                    var response = JSON.parse(this.response);
                    title = response.title
                    message = response.message
                    status = response.status
                }
                Swal.fire({
                    title: title,
                    text: message,
                    type: status,
                    confirmButtonClass: 'btn btn-primary',
                    buttonsStyling: false,
                });
                success_btn.prop("disabled", true);
                success_btn.addClass('btn-outline-success')
                success_btn.removeClass('btn-success')
            }
            var form = new FormData();
            form.append('file', file_object, file_object.name);
            var token = $('input[name="csrfmiddlewaretoken"]').val()
            form.append('csrfmiddlewaretoken', token);
            xhr.send(form);
        });
        this.on("error", function (file, response) {
            $(file.previewElement).addClass("dz-error").find('.dz-error-message').text(response.message);
        })

        this.on("success", function (file) {
            success_btn.prop("disabled", false);
            success_btn.removeClass('btn-outline-success')
            success_btn.addClass('btn-success')
            file_object = file
        })
        this.on("maxfilesexceeded", function (file) {
            let error_message = 'Лимит загрузки файла: 1'
            $(file.previewElement).addClass("dz-error").find('.dz-error-message').text(error_message);

        })
    },
    maxThumbnailFilesize: 1, // MB
    addRemoveLinks: true,
    autoDiscover: false,
    dictRemoveFile: " Удалить",
    acceptedFiles: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
})


$('.history-upload-table').DataTable();