/*=========================================================================================
    File Name: data-list-view.js
    Description: List View
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(document).ready(function () {
    "use strict"
    // init thumb view datatable
    let url = '/settings/group/delete/'
    var dataThumbView = $(".data-thumb-view").DataTable({
        responsive: false,
        columnDefs: [
            {
                orderable: true,
                targets: 0,
                checkboxes: {selectRow: true}
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
                    $(this).removeClass("btn-secondary")
                    $(".add-new-data").addClass("show")
                    $(".overlay-bg").addClass("show")
                },
                className: "btn-outline-primary"
            }
        ],
        initComplete: function (settings, json) {
            $(".dt-buttons .btn").removeClass("btn-secondary")
        }
    })

    dataThumbView.on('draw.dt', function () {
        delete_confirm(dataThumbView, url)
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
        $("#rank-title, #rank-order-id, #rank-id").val("");
        $('#edit-text').hide();
        $('#add-new-text').show();
        $('#save_btn').text('Сохранить')
    })

    // On Edit
    $('.action-edit').on("click", function (e) {
        var id = $(this).attr('id');
        e.stopPropagation();
        $('#group-title').val($('#rank-title-' + id).html());
        $('#group-id').val(id);
        var status = ($('#status-' + id).html() === 'Активный') ? true : false
        $('#group-status').attr("checked", status);
        $(".add-new-data").addClass("show");
        $(".overlay-bg").addClass("show");
        $('#edit-text').show();
        $('#add-new-text').hide()
        $('#save_btn').text('Обновить')
    });

    delete_confirm(dataThumbView, url)

    // mac chrome checkbox fix
    if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
    }
})
