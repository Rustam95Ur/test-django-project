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
    let url = '/settings/delete/'

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
        order: [[0, "asc"]],
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
    var kpi_val_option = $("select[name='type_id'] option[value='1']"),
        progress_val_option = $("select[name='type_id'] option[value='2']");
    // Close sidebar
    $(".hide-data-sidebar, .cancel-data-btn, .overlay-bg").on("click", function () {
        $(".add-new-data").removeClass("show");
        $(".overlay-bg").removeClass("show");
        $("#col_name, #setting-title, #setting-value, #setting-id").val("");
        $('option:selected', '#setting-type-val').removeAttr('selected');
        $('option:selected', '#setting-group-id').removeAttr('selected');
        $("#setting-type, #setting-type-val, #setting-group-id").prop("selectedIndex", 0);
        kpi_val_option.removeAttr("disabled");
        kpi_val_option.removeAttr("selected");
        progress_val_option.removeAttr("selected");
        progress_val_option.removeAttr("disabled");
        $('#edit-text').hide();
        $('#add-new-text').show();
        $('#save_btn').text('Сохранить')
        $('#col_name_input').hide()
        $('#progress_inputs').hide()
        $('#kpi_inputs').hide()
        $('#for_progress').hide()
        $('#for_kpi').hide()
        $('input[name="change_type_val"]').val(0)
    })

    // On Edit
    $('.action-edit').on("click", function (e) {
        var id = $(this).attr('id'),
            type = $('#setting-type-' + id).attr('data-type'),
            type_val = $('#setting-type-val-' + id).attr('data-type-val'),
            group_id = $('#setting-group-' + id).attr('data-group');
        e.stopPropagation();
        if (parseInt(type) === 1) {
            kpi_val_option.attr("selected", "selected");
            progress_val_option.attr("disabled", "disabled");
            $("select[name='type_val'] option[value='" + type_val + "']").attr("selected", "selected");
            $("select[name='group'] option[value='" + group_id + "']").attr("selected", "selected");

            $('#kpi_inputs').show()
            $('#for_kpi').show()
        } else if (parseInt(type) === 2) {
            $('#progress_inputs').show()
            $('#for_progress').show()
            $('#setting-value').val($('#setting-value-' + id).html());
            kpi_val_option.attr("disabled", "disabled");
            progress_val_option.attr("selected", "selected");
        }
        $('#setting-id').val(id)
        $('#col_name_input').show()
        $('#setting-title').val($('#setting-title-' + id).html());
        $('#col_name').val($('#setting-col-name-' + id).html());
        $(".add-new-data").addClass("show");
        $(".overlay-bg").addClass("show");
        $('#edit-text').show();
        $('#add-new-text').hide()
        $('#save_btn').text('Обновить')
    });

    // // On Delete
    // $('.action-delete').on("click", function (e) {
    //     e.stopPropagation();
    //     $(this).closest('td').parent('tr').fadeOut();
    // });

    $('select[name="type_id"]').on('change', function () {
        var id = $(this).val()
        $('#col_name_input').show()
        if (parseInt(id) === 1) {
            $('#kpi_inputs').show()
            $('#for_kpi').show()
            $('#for_progress').hide()
            $('#progress_inputs').hide()
        } else if (parseInt(id) === 2) {
            $('#for_kpi').hide()
            $('#for_progress').show()
            $('#kpi_inputs').hide()
            $('#progress_inputs').show()
        }

    })
    $('select[name="type_val"]').on('change', function () {
         $('input[name="change_type_val"]').val(1)
    })
// delete confirm
    delete_confirm(dataThumbView, url)

    // mac chrome checkbox fix
    if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
    }
})
