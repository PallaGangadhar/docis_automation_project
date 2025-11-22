var pass = 0;
var fail = 0;
var total = 0;
var chart = "";
var no_run = 0;
var total_tc_selected = 0;
var iter = 0;
var testcase_selected = 0;

$('#TC').on("click", "button", function () {
    data = $(this).val();
    $.ajax({
        url: "/",
        type: "POST",
        data: { 'data': data },

    });
});

$(document).ready(function () {
    $('.testcases').click(function () {
        $('#select_all').prop('checked', false);
    });
    $('.modules').click(function () {
        $('#select_module').prop('checked', false);
        if ($('#select_all').is(':checked') == true) { maintain_testcase_selection() }
    });
});

function maintain_testcase_selection() {
    module_id_arr = removeDuplicates(module_id_arr)
    for (let m = 0; m < module_id_arr.length; m++) {
        $("input:checkbox[name='testcase_module_" + module_id_arr[m] + "[]']").prop('checked', true);
    }
    checkboxes_value_1 = count_selected_testcases();
    $('#total_tc_count').text(checkboxes_value_1.length.toString());
    $('#tc_count b').text("Total TC Selected: " + checkboxes_value_1.length.toString());
}

$('#stop').click(function () {
    $('#clear_logs').prop('disabled', false);
    $('#stop').prop('disabled', true);
    $.ajax({
        url: "/stop",
        method: "POST",
        data: { "stop": "Stop" },
        success: function () {

        }
    });
});

$('#clear_logs').click(function () {
    location.reload();
});


// $(document).ready(function () {
//     // var socket = io.connect('http://' + document.domain + ':' + location.port);
//     var socket = io.connect('http://' + document.domain + ':' + location.port, {
//         reconnection: true,         // Enable reconnection
//         reconnectionAttempts: 5,     // Number of reconnection attempts
//         reconnectionDelay: 1000      // Delay between reconnection attempts
//     });

//     // Register session after initial connection
//     socket.on('connect', function () {
//         socket.emit('register_session', { url: window.location.href });
//     });

//     // Re-register session after reconnection
//     socket.on('reconnect', function (attempt) {
//         console.log('Reconnected to server after attempt', attempt);
//         socket.emit('register_session', { url: window.location.href });
//     });

//     socket.on('message', function (msg, cb) {
//         console.log("messhh")
//         var color = 'black';
//         console.log(msg)

//     });

//     socket.on('charts_details', function (msg) {
//         var pass_per = 0.0
//         var fail_per = 0.0
//         var no_run_per = 0.0

//         total = msg.pass_tc + msg.fail_tc
//         total_tc_selected = msg.total_count

//         pass_per = (msg.pass_tc / total_tc_selected) * 100
//         fail_per = (msg.fail_tc / total_tc_selected) * 100
//         no_run = total_tc_selected - (total)

//         no_run_per = (no_run / total_tc_selected) * 100
//         $('#total_tc_count').text(total_tc_selected);
//         $('#total_pass_count').text(msg.pass_tc);
//         $('#total_fail_count').text(msg.fail_tc);
//         $('#no_run_count').text(no_run);
//         $('#tc_count b').text("Total TC Selected: " + total_tc_selected);
//         chart.series[0].setData([
//             { name: msg.pass_tc + ' PASS', y: pass_per, color: "#00FF00" },
//             { name: msg.fail_tc + ' FAIL', y: fail_per, color: "#FF0000" },
//             { name: no_run + ' No Run', y: no_run_per, color: "#2E2EFF" },
//         ], true);

//         if (total == total_tc_selected) {
//             $('#stop').prop('disabled', true);
//             $('#clear_logs').prop('disabled', false);
//             $('#tc_status').text("Completed");
//             iter = 0;
//         }

//     });

//     socket.on('disconnect', () => {
//         socket.emit('client disconnected')
//     });
// });



// function show_charts(pass_per, fail_per, pass, fail){





$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});


var checkboxes_value = [];
var uncheckboxes_value = [];
var module_id = "";
var module_id_arr = [];
var testcase_names = [];
var testcase_id = []

$("input:checkbox[name='modules[]']").click(function () {
    select_testcases()
});

$("#select_module").click(function () {
    $(".modules").prop('checked', $(this).prop('checked'));
    $("#select_all").prop('checked', false);
    select_testcases()

});


function removeDuplicates(arr) {
    return arr.filter((item,
        index) => arr.indexOf(item) === index);
}

function select_testcases() {

    var modules = [];
    var check_module_id = "";
    $('#tc_select').prop('checked', false);
    $("#tc_select").css('display', 'none');
    $('.testcases').prop('checked', false);
    $('#tc_count b').text("Total TC Selected: 0");
    $('#total_tc_count').text("0");


    $("input:checkbox[name='modules[]']:checked").each(function () {
        modules.push($(this).attr("id"));
        check_module_id = $(this).attr("id");
    });


    $("input:checkbox[name='modules[]']:not(:checked)").each(function () {
        unchecked_module = $(this).attr("id");
        uncheckboxes_value.push($(this).attr("id"));
        $(".show_" + unchecked_module).css('display', 'none');

    });
    for (let i = 0.; i < modules.length; i++) {
        module_id = modules[i].replace(/[^\d.]/g, '');
        module_id_arr.push(module_id)
        if ($("#module_" + module_id).is(":checked") == true) {
            $(".show_module_" + module_id).css('display', 'block');
            $("#tc_select").css('display', 'block');
            uncheckboxes_value = removeDuplicates(uncheckboxes_value)
            remove_err_ele(uncheckboxes_value, modules[i]);
        }

    }
    module_id_arr = removeDuplicates(module_id_arr)
    for (let k = 0; k < uncheckboxes_value.length; k++) {
        unchecked_module_id = uncheckboxes_value[k].replace(/[^\d.]/g, '');
        remove_err_ele(module_id_arr, unchecked_module_id)
    }

}

$('#check_tc').click(function () {
    checkboxes_value_1 = count_selected_testcases()
    if (checkboxes_value_1.length == 0) {
        alert("Please select atleast one TC..")
        var divelement = document.getElementById("exampleModal");
        divelement.style.display = 'none';
    }
});
function show_modal(div_id) {
    var divelement = document.getElementById(div_id);
    divelement.style.display = 'block';
}
function close_window(div_id) {
    var divelement = document.getElementById(div_id);
    divelement.style.display = 'none';
}


function run_tc(div_id) {
    var text = $('#regression_name').val();
    var cmts_type = $("input[name=cmts_type]").val()
    var device_id = $("input[name=device_id]").val()

    const checkboxes = document.querySelectorAll(".testcases:checked"); // Select all checkboxes with class 'checkbox'
    checkboxes.forEach(checkbox => {
        testcase_id.push(checkbox.dataset.attr)
    });
    testcase_id = removeDuplicates(testcase_id)
    $('#tc_status').text("In Progres");
    if (text == "") {
        alert('Please enter regression name...')
    }
    else {
        module_id_arr = removeDuplicates(module_id_arr)
        for (let k = 0; k < uncheckboxes_value.length; k++) {
            unchecked_module_id = uncheckboxes_value[k].replace(/[^\d.]/g, '');
            remove_err_ele(module_id_arr, unchecked_module_id)
        }
        for (let m = 0; m < module_id_arr.length; m++) {
            $("input:checkbox[name='testcase_module_" + module_id_arr[m] + "[]']").each(function () {
                if (this.checked) {
                    testcase_names.push($(this).next('label').text());
                    checkboxes_value.push($(this).val());
                }
            });
        }

        if (checkboxes_value.length == 0) {
            alert("Please select atleast one TC..")
            var divelement = document.getElementById(div_id);
            divelement.style.display = 'none';
        }
        else {
            var divelement = document.getElementById(div_id);
            divelement.style.display = 'none';
            total_tc_selected = checkboxes_value.length;
            checkboxes_value = checkboxes_value.toString();
            testcase_id = testcase_id.toString()
            testcase_names = testcase_names.toString();
            $('#stop').prop('disabled', false);
            $('#check_tc').prop('disabled', true);
            $('#tc_count b').text("Total TC Selected: " + total_tc_selected);
            $('#total_tc_count').text(total_tc_selected);
            console.log(testcase_id)
            // var random_string = generateRandomAlphanumeric(15);
            // window.location.href = "/tc_execution/" + device_id + "?" + random_string
            // $.ajax({
            //     url: "/tc_execution/" + device_id + "?" + random_string,
            //     method: "POST",
            //     data: { "data": checkboxes_value, 'regression_name': text, 'total_tc_selected': total_tc_selected, 'cmts_type': cmts_type, "device_id": , 'random_string': random_string, 'testcase_id': testcase_id }
            // });
        }
    }

}


$('.testcases').on('change', function () {
    checkboxes_value_1 = count_selected_testcases()
    $('#total_tc_count').text(checkboxes_value_1.length.toString());
    $('#tc_count b').text("Total TC Selected: " + checkboxes_value_1.length.toString());
});

$('#select_all').click(function () {
    $(".testcases").prop('checked', $(this).prop('checked'));
    checkboxes_value_1 = count_selected_testcases();
    $('#total_tc_count').text(checkboxes_value_1.length.toString());
    $('#tc_count b').text("Total TC Selected: " + checkboxes_value_1.length.toString());
});
$("input:checkbox[name='modules[]']").click(function () {
    checkboxes_value_1 = count_selected_testcases();
    $('#total_tc_count').text(checkboxes_value_1.length.toString());
    $('#tc_count b').text("Total TC Selected: " + checkboxes_value_1.length.toString());
});


function count_selected_testcases() {
    checkboxes_value_1 = []
    module_id_arr = removeDuplicates(module_id_arr)
    for (let m = 0; m < module_id_arr.length; m++) {
        $("input:checkbox[name='testcase_module_" + module_id_arr[m] + "[]']").each(function () {
            if (this.checked) {
                checkboxes_value_1.push($(this).val());
            }
        });
    }

    return checkboxes_value_1;
}

function remove_err_ele(array, val) {
    const index = array.indexOf(val);
    if (index > -1) {
        array.splice(index, 1)
    }
    // console.log(array);
    return array;
}


function clear_filter() {
    window.location.href = window.location.href.split("?")[0]
}

$(function () {
    $("#from_date").datepicker({
        autoclose: true,
        todayHighlight: true
    }).datepicker();

});
$(function () {
    $("#to_date").datepicker({
        autoclose: true,
        todayHighlight: true
    }).datepicker();
});
try {
    date = window.location.href
    from_date = date.split('?')[1].split('&')[0].split('=')[1]
    to_date = date.split('?')[1].split('&')[1].split('=')[1]
    $('#from_date_val').val(from_date);
    $('#to_date_val').val(to_date);
}
catch (err) {
    console.log(err)
}

// var testcase_id = [];

// $("input:checkbox[name='reg_box']").on('change', function () {
//     if (this.checked) {
//         testcase_id.push($(this).val());
//     }
//     else {
//         remove_err_ele(testcase_id, $(this).val());
//     }
// });

// function delete_selected_regression() {
//     console.log("====",testcase_id)
//     if (testcase_id.length == 0) {
//         alert('Please select atleast one testcase')
//     }
//     else {
//         testcase_id = testcase_id.toString();
//         $.ajax({
//             url: "/delete_selected_regression",
//             method: "POST",
//             data: { "data": testcase_id },
//             success: function () {
//                 location.reload();
//             }
//         });
//     }
// }

try {
    var selected_value = window.location.href.split('?')[1].split('=')[1].split('&')[0]
    var search_reg = window.location.href.split('?')[1].split('&')[1].split('=')[1]
    selected_value = selected_value.replace("+", " ")
    $("#cmts_type_filter").val(selected_value);
    search_reg = search_reg.replace(/[+]/g, ' ');
    $("#search_reg").val(search_reg);
}
catch (err) {
}


$(document).on("click", ".edit-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    var device_name = $('#device_' + pk).html();
    var ip = $('#ip_' + pk).html();
    var model = $('#model_' + pk).html();
    var vendor = $('#vendor_' + pk).html();
    $('input[name="device_name"]').val(device_name);
    $('input[name="device_ip"]').val(ip);
    $('input[name="model"]').val(model);
    $('input[name="vendor"]').val(vendor);
    $('#edit_device_details_form').attr('action', '/edit_device_details/' + pk);
    // $("#delete_regression").click(function(){
    //   $("#delete").attr("action", "/delete_regression/" + pk);
    // }); 
});

$(document).on("click", ".open-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    $("#delete_regression").click(function () {
        $("#delete").attr("action", "/delete_regression/" + pk);
    });
});


$(document).on("click", ".tc_delete_open-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    $("#delete_testcase").click(function () {
        $("#delete_tc_form").attr("action", "/delete_testcase/" + pk);
    });
});

$(document).on("click", ".modules_delete_open-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    $("#delete_module").click(function () {
        $("#delete_module_form").attr("action", "/delete_module/" + pk);
    });
});

$(document).on("click", ".device_delete_open-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    $.ajax({
        url: "/show_details_mapped_to_devices",
        method: "POST",
        data: { "data": pk },
        success: function (data) {
            $('#show_details_table').html(data);
        }
    });
    $("#delete_device").click(function () {
        $("#delete_device_form").attr("action", "/delete_device/" + pk);
    });
});

$(document).on("click", ".module_delete_open-ConfirmationDialog", function () {
    var pk = $(this).data('id');
    $.ajax({
        url: "/show_details_mapped_to_modules",
        method: "POST",
        data: { "data": pk },
        success: function (data) {
            $('#show_details_table').html(data);
        }
    });
    $("#delete_module").click(function () {
        $("#delete_module_form").attr("action", "/delete_module/" + pk);
    });
});

$('#select_all_regression').on('click', function () {
    $(".reg_box").prop('checked', $(this).prop('checked'));
    $("input:checkbox[name='reg_box']:checked").each(function () {
        testcase_id.push($(this).val());
    });
});

try {
    var selected_module = window.location.href.split('?')[1].split('=')[1].split('&')[0]
    var selected_device = window.location.href.split('?')[1].split('&')[1].split('=')[1]
    var search_tc = window.location.href.split('?')[1].split('&')[2].split('=')[1]
    selected_value = selected_value.replace("+", " ")
    $("#module_type_filter").val(selected_module);
    $("#device_type_filter").val(selected_device);
    search_tc = search_tc.replace(/[+]/g, ' ');
    $("#search_tc").val(search_tc);
}
catch (err) {
}

try {
    var selected_device = window.location.href.split('?')[1].split('=')[1].split('&')[0]
    var search_module = window.location.href.split('?')[1].split('&')[1].split('=')[1]
    $("#device_type_filter").val(selected_device);
    search_module = search_module.replace(/[+]/g, ' ');
    $("#search_module").val(search_module);
}
catch (err) {
}


try {
    var check_for_page = window.location.href.split('?')[1].split('=')[0]
    if (check_for_page != 'page') {
        search_device = window.location.href.split('?')[1].split('=')[1].split('&')[0]
    }
    search_device = search_device.replace(/[+]/g, ' ');
    $("#search_device").val(search_device);
}
catch (err) {
}


function generateRandomAlphanumeric(length) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}

// Example usage:
// Adjust length as needed
try {
    $('#device_type_filter').on('change', function () {
        var device_id = this.value;
        $.ajax({
            url: "/get_module_details",
            method: "POST",
            data: { "data": device_id },
            success: function (data) {
                $('#module_type_filter').html(data);
            }
        });
    });
}
catch (err) { }



try {
    var url = window.location.href
    module_id = ""
    device_id = ""
    try {
        module_id = url.split('module_type_dropdown=')[1].split('&')[0]
    }
    catch (err) { }
    try {
        device_id = url.split('device_type_dropdown=')[1].split('&')[0]
    }
    catch (err) { }
    $.ajax({
        url: "/get_selected_module_details",
        method: "POST",
        data: { "module_id": module_id, 'device_id': device_id },
        success: function (data) {
            $('#module_type_filter').html(data);
        }
    });

}
catch (err) { }

$(document).ready(function () {
    // Initialize Datepicker
    $('#from_date, #to_date').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        todayHighlight: true
    });

    // Capture Date Selection
    $('#from_date_val').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    }).on('changeDate', function (e) {
        $('#from_date_val').val(
            e.format('yyyy-mm-dd')
        );
    });

    $('#to_date_val').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true
    }).on('changeDate', function (e) {
        $('#to_date_val').val(
            e.format('yyyy-mm-dd')
        );
    });

});


$(".rereun_tc").click(function () {
    var tc_id = $("input[name=tc_id]").val()
    var log_id = $("input[name=log_id]").val()
    var regression_string = generateRandomAlphanumeric(15);
    $('#log_content').attr('id', 'log_content_' + regression_string);

    window.location.href = "/rerun_tc/" + log_id + "?" + regression_string

    $.ajax({
        url: "/rerun_tc/" + log_id + "?" + regression_string,
        method: "POST",
        data: { "tc_id": tc_id, 'log_id': log_id, 'random_string': regression_string }
    },
        success = function () {
            console.log("success === ", regression_string);

        }
    );

});


$('#multiple_case').click(function () {
    let visibility_check_checkbox = $("input:checkbox[name='rereun_mutltiple_tc']");
    visibility_check = visibility_check_checkbox.css("visibility") == "hidden";
    if (visibility_check) {
        $("input:checkbox[name='rereun_mutltiple_tc']").css('visibility', 'visible');
    }
    else {
        $("input:checkbox[name='rereun_mutltiple_tc']").css('visibility', 'hidden');
        let checkboxes = document.getElementsByName("rereun_mutltiple_tc");
        checkboxes.forEach(cb => cb.checked = false);

        // for (let i = 0; i < checkboxes.length; i++) {
        //     checkboxes[i].checked = false;
        // }
    }

});


$('#rereun_mutltiple_tc').click(function () {
    const testcase_ids = []; // Your existing array
    const logs_ids = []; // Your existing array
    const checkboxes = document.querySelectorAll('input[name="rereun_mutltiple_tc"]:checked');
    var reg_id = 0;
    // var log_id = $("input[name=log_id]").val()
    checkboxes.forEach(cb => {
        testcase_ids.push(cb.value.split(',')[0]);
        logs_ids.push(cb.value.split(',')[1]);
        reg_id = cb.value.split(',')[2];
    });
    // let log_id_list = $("input[name='log_id']").map(function() {
    //     return $(this).val();
    // }).get();

    total_rerun_count = testcase_ids.length

    rerun_tc_list = testcase_ids.toString();
    log_id_list = logs_ids.toString();
    $.ajax({
        url: "/track_rerun_tc",
        method: "POST",
        data: { "tc_id": rerun_tc_list, "reg_id": reg_id, "total_rerun_tc": total_rerun_count },
        success: function () {
            var regression_string = generateRandomAlphanumeric(15);
            window.location.href = "/rerun_tc?reg_id=" + reg_id + "&random_string=" + regression_string+"&total_rerun_count="+total_rerun_count
            $.ajax({
                url: "/rerun_tc?reg_id=" + reg_id + "&random_string=" + regression_string,
                method: "POST",
                data: { "tc_id": rerun_tc_list, "log_id": log_id_list, "total_rerun_tc": total_rerun_count }
            });
        }
    });
})





