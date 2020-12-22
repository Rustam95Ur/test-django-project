$(document).ready(function () {
    "use strict"
    // init list view datatable
    var dataListView = $(".data-list-view").DataTable({
        responsive: false,
        columnDefs: [
            {
                orderable: false,
                targets: 0,
                checkboxes: {selectRow: false, selectAll: false}
            }
        ],
        dom:
            '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
        oLanguage: {
            sLengthMenu: "_MENU_",
            sSearch: ""
        },
        aLengthMenu: [[4, 10, 15, 20], [4, 10, 15, 20]],
        select: {
            style: "multi"
        },
        order: [[1, "asc"]],
        bInfo: false,
        pageLength: 4,
        buttons: [
            {
                text: "<i class='feather icon-plus'></i> Добавить",
                action: function () {
                    $(this).removeClass("btn-secondary");
                    $(".add-new-data").addClass("show");
                    $(".overlay-bg").addClass("show");
                    $("#data-name, #data-price").val("");
                    $("#data-category, #data-status").prop("selectedIndex", 0)
                },
                className: "btn-outline-primary"
            }
        ],
        initComplete: function (settings, json) {
            $(".dt-buttons .btn").removeClass("btn-secondary")
        }
    });

    dataListView.on('draw.dt', function () {
        setTimeout(function () {
            if (navigator.userAgent.indexOf("Mac OS X") != -1) {
                $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
            }
        }, 50);
    });

    // To append actions dropdown before add new button
    var actionDropdown = $(".actions-dropodown")
    actionDropdown.insertBefore($(".top .actions .dt-buttons"))


    // Scrollbar
    if ($(".data-items").length > 0) {
        new PerfectScrollbar(".data-items", {wheelPropagation: false})
    }

    // Close sidebar
    $(".hide-data-sidebar, .cancel-data-btn, .overlay-bg").on("click", function () {
        $(".add-new-data").removeClass("show");
        $(".overlay-bg").removeClass("show");
        $("#data-title, #data-id").val("");
        $("#data-category, #data-status").prop("selectedIndex", 0);
        $('#edit-text').hide();
        $('#add-new-text').show();
        $("#data-type").find('option').attr("selected",false) ;
        $('#save_btn').text('Сохранить')
    })

    // On Edit
    $('.action-edit').on("click", function (e) {
        var id = $(this).attr('id');
        e.stopPropagation();
        $('#data-title').val($('#data-' + id).html());
        $('#data-id').val(id);
        $(".add-new-data").addClass("show");
        $(".overlay-bg").addClass("show");
        $('#edit-text').show();
        $('#add-new-text').hide()
        $('#save_btn').text('Обновить')
    });

    // On Delete
    // $('.action-delete').on("click", function(e){
    //   e.stopPropagation();
    //   $(this).closest('td').parent('tr').fadeOut();
    // });

    // dropzone init
    // Dropzone.options.dataListUpload = {
    //   complete: function(files) {
    //     var _this = this
    //     // checks files in class dropzone and remove that files
    //     $(".hide-data-sidebar, .cancel-data-btn, .actions .dt-buttons").on(
    //       "click",
    //       function() {
    //         $(".dropzone")[0].dropzone.files.forEach(function(file) {
    //           file.previewElement.remove()
    //         })
    //         $(".dropzone").removeClass("dz-started")
    //       }
    //     )
    //   }
    // }
    // Dropzone.options.dataListUpload.complete()

    // mac chrome checkbox fix
    if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
    }

    // delete confirm
    let url = '/customers/type/delete/'
    delete_confirm(dataListView, url)

})

