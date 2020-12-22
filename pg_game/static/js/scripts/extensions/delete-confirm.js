function delete_confirm(dataListView, url) {
    $('.delete_confirm').on('click', function () {
        let item = this;
        let data_id = $(this).attr('id')
        data_id = data_id.replace('data-delete-', '')


        Swal.fire({
            title: 'Вы уверены?',
            text: "Вы не сможете отменить это!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Да, удалить!',
            cancelButtonText: 'Отмена',
            confirmButtonClass: 'btn btn-primary',
            cancelButtonClass: 'btn btn-danger ml-1',
            buttonsStyling: false,
        }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: url + data_id,
                    type: "GET",
                    dataType: "json",
                    success: function (response) {
                        $(item).closest('tr').remove();
                        dataListView
                            .row($(item).parents('tr'))
                            .remove()
                            .draw();
                        Swal.fire(
                            {
                                type: response.status,
                                title: response.title,
                                text: response.message,
                                confirmButtonClass: 'btn btn-success',
                            }
                        )
                    },
                    error: function (xhr, ajaxOptions, thrownError) {
                        var response = xhr.responseJSON
                        if (response) {
                            Swal.fire(
                                {
                                    type: response.status,
                                    title: response.title,
                                    text: response.message,
                                    confirmButtonClass: 'btn btn-success',
                                }
                            )
                        } else {
                            Swal.fire(
                                {
                                    type: "error",
                                    title: 'Ошибка при удалении!',
                                    text: 'Пожалуйста, попробуйте еще раз. Либо обратитесь к администратору',
                                    confirmButtonClass: 'btn btn-success',
                                }
                            )
                        }

                    }
                });
            }

        })
    });
}
