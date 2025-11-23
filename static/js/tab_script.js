var selectedModules = {};
var selected_testcases_list = {};
var each_tab_tc_count = {}

$(document).ready(function () {
  $(document).on('change', 'select[id^="vendor_select_tab"]', function () {
    const fullId = $(this).attr('id'); // e.g., vendor_select_tab3
    const vendor_active_tab = fullId.replace('vendor_select_', ''); // tab3
    const vendor = $(this).val();

    $.ajax({
      url: "/get_device_details",
      method: "POST",
      data: { data: vendor },
      success: function (data) {
        $('#deviceSelect_' + vendor_active_tab).html(data); // use dynamic deviceSelect ID
      },
      error: function (xhr, status, error) {
        alert("Error: " + error);
      }
    });
  });
});

$(document).ready(function () {
  $(document).on('change', 'select[id^="deviceSelect_tab"]', function () {
    const fullId = $(this).attr('id'); // e.g., vendor_select_tab3
    const device_active_tab = fullId.replace('deviceSelect_', ''); // tab3
    const device = $(this).val();
    const device_name = $('#deviceSelect_' + device_active_tab + ' option:selected').text();
    $('#device_id_' + device_active_tab).val(device);
    $('#cmts_type_' + device_active_tab).val(device_name)
    $.ajax({
      url: "/get_tab_modules_details",
      method: "POST",
      data: { data: device, tab:device_active_tab },
      success: function (data) {
        $('#ul_modules_' + device_active_tab).html(data); // use dynamic deviceSelect ID
        $('#ul_modules_' + device_active_tab).each(function () {
          const ulId = $(this).attr('id'); // e.g., "ul_modules_tab1"
          const tabId = ulId.replace('ul_modules_', ''); // e.g., "tab1"
          const newClass = 'modules_list_class_' + tabId;

          $(this).find('li input[type="checkbox"]').each(function () {
            // Remove any existing "modules_list_tabX" class
            $(this).removeClass(function (index, className) {
              return (className.match(/modules_list_class_tab\d+/g) || []).join(' ');
            });

            // Add the new class
            $(this).addClass(newClass);
          });
        });
      },
      error: function (xhr, status, error) {
        alert("Error: " + error);
      }
    });
  });
});


$(document).ready(function () {
  // Global object to store selected test cases per tab
  // const selected_testcases_list = {};

  // 🟦 Handle "Select All" checkbox click
  $(document).on("change", 'input[id^="select_all_modules_"]', function () {
    const activeTabId = this.id.replace("select_all_modules_", "");
    const isChecked = $(this).is(":checked");

    // Initialize array for this tab
    if (!selectedModules[activeTabId]) selectedModules[activeTabId] = [];
    let module_selected = [];

    // Check/uncheck all checkboxes for this tab
    $(".modules_list_class_" + activeTabId).prop("checked", isChecked);

    if (isChecked) {
      // ✅ Add all checked values (unique, non-empty)
      $(".modules_list_class_" + activeTabId + ":checked").each(function () {
        const val = $(this).val();
        if (val && !module_selected.includes(val)) module_selected.push(val);
      });
    } else {
      // ❌ Unselect all
      module_selected = [];
    }

    selectedModules[activeTabId] = module_selected;
    updateTabModuleInfo(activeTabId, selectedModules);
  });

  // 🟩 Handle individual checkbox click
  $(document).on("change", 'input[type="checkbox"][class*="modules_list_class_"]', function () {
    const fullClass = $(this)
      .attr("class")
      .split(" ")
      .find((cls) => cls.startsWith("modules_list_class_"));
    if (!fullClass) return;

    const activeTabId = fullClass.replace("modules_list_class_", "");
    if (!selectedModules[activeTabId]) selectedModules[activeTabId] = [];

    let module_selected = selectedModules[activeTabId];
    const value = $(this).val();

    if ($(this).is(":checked")) {
      if (value && !module_selected.includes(value)) module_selected.push(value);
    } else {
      module_selected = module_selected.filter((v) => v !== value);
    }

    // 🔄 Auto-toggle "Select All" checkbox
    const total = $(".modules_list_class_" + activeTabId).length;
    const checked = $(".modules_list_class_" + activeTabId + ":checked").length;
    $("#select_all_modules_" + activeTabId).prop("checked", total > 0 && total === checked);

    selectedModules[activeTabId] = module_selected;
    updateTabModuleInfo(activeTabId, selectedModules);
  });

  // 🧠 Update UI for each tab
  function updateTabModuleInfo(activeTabId, selectedModules) {
    $.ajax({
      url: '/get_tab_testcase_details',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ modules: selectedModules[activeTabId], tabid: activeTabId }),
      success: function (data) {
        $('#ul_testcases_' + activeTabId).html(data);

        $('#ul_testcases_' + activeTabId).each(function () {
          const ulId = $(this).attr('id'); // e.g., "ul_modules_tab1"
          const tabId = ulId.replace('ul_testcases_', ''); // e.g., "tab1"
          const newClass = 'testcase_list_class_' + tabId;

          $(this).find('li input[type="checkbox"]').each(function () {
            // Remove any existing "modules_list_tabX" class
            $(this).removeClass(function (index, className) {
              return (className.match(/testcase_list_class_tab\d+/g) || []).join(' ');
            });

            // Add the new class
            $(this).addClass(newClass);
          });
        });


      },
      error: function (xhr) {
        console.error('Error:', xhr.responseText);
      }
    });
  }
});


$(document).ready(function () {
  // Global object to store selected test cases per tab

  // 🟦 Handle "Select All" checkbox click
  $(document).on("change", 'input[id^="select_all_tc_"]', function () {
    const activeTabId = this.id.replace("select_all_tc_", "");
    const isChecked = $(this).is(":checked");

    if (!selected_testcases_list[activeTabId]) selected_testcases_list[activeTabId] = [];
    let tc_selected = [];

    // Check/uncheck all checkboxes in this tab
    $(".testcase_list_class_" + activeTabId).prop("checked", isChecked);

    if (isChecked) {
      $(".testcase_list_class_" + activeTabId + ":checked").each(function () {
        const val = $(this).val();
        if (val && !tc_selected.includes(val)) tc_selected.push(val);
      });
    }

    selected_testcases_list[activeTabId] = tc_selected;
    updateTabInfo(activeTabId, tc_selected);
  });

  // 🟩 Handle individual testcase checkbox click
  $(document).on("change", 'input[type="checkbox"][class*="testcase_list_class_"]', function () {
    const fullClass = $(this)
      .attr("class")
      .split(" ")
      .find((cls) => cls.startsWith("testcase_list_class_"));
    if (!fullClass) return;

    const activeTabId = fullClass.replace("testcase_list_class_", "");
    if (!selected_testcases_list[activeTabId]) selected_testcases_list[activeTabId] = [];

    let tc_selected = selected_testcases_list[activeTabId];
    const value = $(this).val();

    if ($(this).is(":checked")) {
      if (value && !tc_selected.includes(value)) tc_selected.push(value);
    } else {
      tc_selected = tc_selected.filter((v) => v !== value);
    }

    // Auto-toggle "Select All" if all are selected
    const total = $(".testcase_list_class_" + activeTabId).length;
    const checked = $(".testcase_list_class_" + activeTabId + ":checked").length;
    $("#select_all_tc_" + activeTabId).prop("checked", total > 0 && total === checked);

    selected_testcases_list[activeTabId] = tc_selected;
    updateTabInfo(activeTabId, tc_selected);
  });

  // 🧠 Function to update tab UI
  function updateTabInfo(activeTabId, tc_selected) {
    const count = tc_selected.length;

    $("#tc_count_" + activeTabId + " b").text("Total Test Cases Selected: " + count);
    $("#total_tc_count_" + activeTabId).text(count);
    $("#regression_name_" + activeTabId).prop("disabled", count === 0);
    if (count === 0) $("#run_" + activeTabId).prop("disabled", true);

    $("#regression_name_" + activeTabId).on("input", function () {
      $("#run_" + activeTabId).prop("disabled", $(this).val().trim() === "");
    });

    console.log(`✅ [${activeTabId}] Selected Testcases:`, selected_testcases_list[activeTabId]);
  }
});


$(document).ready(function () {
  var socket = io.connect('http://' + document.domain + ':' + location.port, {
    reconnection: true,         // Enable reconnection
    reconnectionAttempts: 5,     // Number of reconnection attempts
    reconnectionDelay: 1000      // Delay between reconnection attempts
  });

  // Register session after initial connection
  socket.on('connect', function () {
    console.log("Connected to server");
  });


  socket.on('message', function (data) {
    $('#log_content_' + data.tab + ' p').html('');
    var color = 'black';
    var eachLine = data.msg.split('\n');
    for (var i = 0, l = eachLine.length; i < l; i++) {


      if ((eachLine[i].trim().includes('TestStep') == true) && (eachLine[i].trim().includes('PASS') == true)) {
        color = "green"
      }
      else if ((eachLine[i].trim().includes('TestStep') == true) && (eachLine[i].trim().includes('FAIL') == true)) {
        color = "red"
      }
      if (data.rerun == 'True') {

        $('#log_content').append('<div style="color:' + color + '">' + $('<div/>').append(eachLine[i].trim().replace(/ /g, "&nbsp;")).html());
      }
      else {
        $('#log_content_' + data.tab).append('<div style="color:' + color + '">' + $('<div/>').append(eachLine[i].trim().replace(/ /g, "&nbsp;")).html());
      }
    }

  });

  socket.on('charts_details', function (msg) {
    var pass_per = 0.0
    var fail_per = 0.0
    var no_run_per = 0.0
    var count = 0

    total = msg.pass_tc + msg.fail_tc
    total_tc_selected = msg.total_count
    tc_execution_count = msg.tc_execution_count


    pass_per = (msg.pass_tc / total_tc_selected) * 100
    fail_per = (msg.fail_tc / total_tc_selected) * 100
    no_run = total_tc_selected - (total)
    no_run_per = (no_run / total_tc_selected) * 100

    var tab_name = msg.tab + '_' + msg.query_string;

    if (msg.rerun == 'True') {
      $('#total_tc_count').text(total_tc_selected);
      $('#total_pass_count').text(msg.pass_tc);
      $('#total_fail_count').text(msg.fail_tc);
      $('#no_run_count').text(no_run);
      $('#tc_count b').text("Total TC Selected: " + total_tc_selected);

      chart = Highcharts.chart('chart_container', {
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          backgroundColor: '#f9f9f9',
          type: 'pie',
          height: 350,
        },
        title: {
          text: '',
          // align: 'cenet'
        },
        exporting: {
          enabled: false // Disables the context menu
        },
        credits: {
          enabled: false // Disables the Highcharts.com text
        },

        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false
            },
            showInLegend: true
          }
        },
        series: [{
          name: null,
          colorByPoint: true,
          data: [{
            name: msg.pass_tc + ' PASS',
            y: pass_per,
            color: "#00FF00"
          }, {
            name: msg.fail_tc + ' FAIL',
            y: fail_per,
            color: '#FF0000'
          },
          {
            name: no_run + ' No Run',
            y: no_run_per,
            color: '#2E2EFF'
          },

          ]
        }]
      });
    }
    else {
      $('#total_tc_count_' + tab_name).text(total_tc_selected);
      $('#total_pass_count_' + tab_name).text(msg.pass_tc);
      $('#total_fail_count_' + tab_name).text(msg.fail_tc);
      $('#no_run_count_' + tab_name).text(no_run);
      $('#tc_count_' + tab_name + ' b').text("Total TC Selected: " + total_tc_selected);
      chart = Highcharts.chart('container_' + tab_name, {
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          backgroundColor: '#f9f9f9',
          type: 'pie',
          height: 350,
        },
        title: {
          text: '',
          // align: 'cenet'
        },
        exporting: {
          enabled: false // Disables the context menu
        },
        credits: {
          enabled: false // Disables the Highcharts.com text
        },

        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: false
            },
            showInLegend: true
          }
        },
        series: [{
          name: null,
          colorByPoint: true,
          data: [{
            name: msg.pass_tc + ' PASS',
            y: pass_per,
            color: "#00FF00"
          }, {
            name: msg.fail_tc + ' FAIL',
            y: fail_per,
            color: '#FF0000'
          },
          {
            name: no_run + ' No Run',
            y: no_run_per,
            color: '#2E2EFF'
          },

          ]
        }]
      });
    }


    btn_color = ''

    if (msg.status == 'PASS') { btn_color = 'success' }

    else { btn_color = 'danger' }
    $(`#summary_table_${tab_name} tr:eq(${tc_execution_count}) td:eq(2)`).html(`<button class='btn btn-outline-${btn_color} btn-sm'>${msg.status}</button>`);
    // for (var i = 1; i <= total_tc_selected; i++) {
    //   $(`#summary_table_${tab_name} tr:eq(${i}) td:eq(2)`).text(msg.status);
    // }
  });
});

try {
  $(document).ready(function () {
    chart = Highcharts.chart('container_tab1', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        height: 350,
        backgroundColor: '#f9f9f9'
      },
      title: {
        text: '',
        // align: 'cenet'
      },
      exporting: {
        enabled: false // Disables the context menu
      },
      credits: {
        enabled: false // Disables the Highcharts.com text
      },

      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: null,
        colorByPoint: true,
        data: [{
          name: '0 Pass',
          y: 0,
          color: "#00FF00"
        }, {
          name: '0 FAIL',
          y: 0,
          color: '#FF0000'
        },
        {
          name: "No Run",
          y: 100,
          color: '#2E2EFF'
        },

        ]
      }]
    });
  });

}
catch (err) { }

try {
  $(document).ready(function () {
    chart = Highcharts.chart('chart_container', {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        height: 350,
        backgroundColor: '#f9f9f9'
      },
      title: {
        text: '',
        // align: 'cenet'
      },
      exporting: {
        enabled: false // Disables the context menu
      },
      credits: {
        enabled: false // Disables the Highcharts.com text
      },

      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          dataLabels: {
            enabled: false
          },
          showInLegend: true
        }
      },
      series: [{
        name: null,
        colorByPoint: true,
        data: [{
          name: '0 Pass',
          y: 0,
          color: "#00FF00"
        }, {
          name: '0 FAIL',
          y: 0,
          color: '#FF0000'
        },
        {
          name: "No Run",
          y: 100,
          color: '#2E2EFF'
        },

        ]
      }]
    });
  });

}
catch (err) { }


function generateRandomAlphanumeric(length) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function run(tab_id) {
  const active_tab = tab_id.id.replace("run_", "");
  var testcase_list = selected_testcases_list[active_tab];
  var modules_list = selectedModules[active_tab]
  total_testcase_selected = testcase_list.length;
  var regression_name = $('#regression_name_' + active_tab).val();
  var device_id = $('#device_id_' + active_tab).val();
  var cmts_type = $('#cmts_type_' + active_tab).val();
  var random_string = generateRandomAlphanumeric(15);
  var tab_name = active_tab + '_' + random_string;
  $('#random_string_' + active_tab).val(random_string);
  $('#log_content_' + active_tab).attr('id', 'log_content_' + tab_name);
  $('#container_' + active_tab).attr('id', 'container_' + tab_name);
  $('#tc_count_' + active_tab).attr('id', 'tc_count_' + tab_name);
  $('#total_tc_count_' + active_tab).attr('id', 'total_tc_count_' + tab_name);
  $('#total_pass_count_' + active_tab).attr('id', 'total_pass_count_' + tab_name);
  $('#total_fail_count_' + active_tab).attr('id', 'total_fail_count_' + tab_name);
  $('#summary_table_' + active_tab).attr('id', 'summary_table_' + tab_name);
  $('#total_tc_count_' + tab_name).text(total_testcase_selected);
  $('#tc_count_' + tab_name + ' b').text('Total Test Cases Selected: ' + total_testcase_selected);
  $.ajax({
    url: "/tc_execution",
    method: "POST",
    data: {
      'testcase_id': testcase_list.toString(),
      "regression_name": regression_name,
      "device_id": device_id,
      "cmts_type": cmts_type,
      "total_tc_selected": total_testcase_selected,
      "random_string": random_string,
      "tab": active_tab
    }
  });

  $.ajax({
    url: "/get_tc_execution_status",
    method: "GET",
    data: { "testcase_id": testcase_list.toString(), "active_tab": active_tab, 'tab_name': tab_name, 'random_string': random_string, 'modules_list': modules_list.toString() },
    success: function (data) {
      $(`#summary_table_${tab_name}`).html(data);

    }
  });
}
$(document).on('click', '.summary_table .pagination a', function (e) {
  e.preventDefault(); // Stop default link navigation

  // ✅ Extract page number from href
  const href = $(this).attr('href');
  const params = new URLSearchParams(href.split('?')[1]);
  const page = params.get('page');
  // 🔁 These must come from context or global variables
  const testcase_id = params.get('testcase_id');  // "30,34,33,32,115"
  const active_tab = params.get('active_tab');    // "tab1"
  const tab_name = params.get('tab_name');        // "tab1_NgYdJvCveTcP9sZ"
  const random_string = params.get('random_string');        // "tab1_NgYdJvCveTcP9sZ"

  // Optional: Convert testcase_id to an array
  const testcase_list = testcase_id ? testcase_id.split(',') : [];

  if (!page || !tab_name || !active_tab || !testcase_list) {
    console.warn("Missing parameters for AJAX pagination");
    return;
  }

  // ✅ AJAX call to get new data
  $.ajax({
    url: "/get_tc_execution_status",
    method: "GET",
    data: {
      "testcase_id": testcase_list.toString(),
      "active_tab": active_tab,
      "tab_name": tab_name,
      "random_string": random_string,
      "page": page
    },
    success: function (data) {
      $(`#summary_table_${tab_name}`).html(data); // Replace table + pagination
    },
    error: function (xhr, status, error) {
      console.error("Pagination AJAX Error:", error);
    }
  });
});

$(document).on("click", ".close-tab", function (e) {
  e.stopPropagation();
  const tabId = $(this).data("tab");
  addJobTab(closed=true, tab_count=tabId);
  $(`#${tabId}-tab`).closest("li").remove();
  $(`#${tabId}`).remove();
  tabCount--;
  // $(`#tab-${tabCount}`).addClass('tab-pane fade');
  

  for (let i = 0; i < $('#myTab button').length; i++) {
    const btn = $('#myTab button').eq(i);
    const div_change = $('#myTabContent .tab-pane').eq(i);
    if(i==0){
      btn.attr("id", "tab1-tab"); 
      btn.attr("data-bs-target", "#tab1" );        // change id
    }       // change id
    else{
      btn.attr("id", "tab" + (i + 1) + "-tab"); 
      btn.attr("data-bs-target", "#tab" + (i + 1));    
      div_change.attr("id", "tab" + (i + 1));
    }
    btn.text("Execution " + (i + 1));
    if (i > 0) {
      btn.append(
        `<span class="ms-2 text-danger close-tab" data-tab="tab${i + 1}" style="cursor:pointer;">&times;</span>`
      );
    }
    
  }
  $(`#tab${tabCount}-tab`).click()
});

let selectedItems = new Set();

$(document).on('change', '.reg_box', function () {
  const id = $(this).val();
  if ($(this).is(":checked")) {
    selectedItems.add(id);
  } else {
    selectedItems.delete(id);
  }
});

function delete_selected_regression() {
    if (selectedItems.size == 0) {
        alert('Please select atleast one testcase')
    }
    else {
        $.ajax({
            url: "/delete_selected_regression",
            method: "POST",
            data: { "data": [...selectedItems].toString() },
            success: function () {
                location.reload();
            }
        });
    }
}


$("#main > div.flex-grow-1.overflow-hidden > div > div.row > div > div > div > div.p-3.div_shadow > div > div > nav > ul > li:nth-child(2)").empty().prepend('<a class="page-link active" href="/view_regression_details?page=1">1</a>');
$(document).on('click', '.pagination_regression_table .pagination a', function (e) {
  $(".pagination_regression_table .pagination a").removeClass("active");
  e.preventDefault();

  let url = $(this).attr('href');
  if (!url) return;

  let clickedPage = $(this).text().trim();   // page number clicked

  $("#pagination_regression_table_1").load(url + " #pagination_regression_table_1 > *", function () {

    // Restore checkbox selections
    $(".reg_box").each(function () {
      const id = $(this).val();
      if (selectedItems.has(id)) {
        $(this).prop("checked", true);
      }
    });

    $("#main > div.flex-grow-1.overflow-hidden > div > div.row > div > div > div > div.p-3.div_shadow > div > div > nav > ul > li:nth-child(2)").removeClass("active");

    // Add active only to clicked page
    $(".pagination_regression_table .pagination a").each(function () {
      if ($(this).text().trim() === clickedPage) {
        $(this).addClass("active");
      }
      else {
        $(this).removeClass("active");
      }
    });
  });
});

