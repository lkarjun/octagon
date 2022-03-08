$("#dataAnalysis").submit((e)=>{
    e.preventDefault()
    dataAnalysis()
})

function append_student_name(data){
    $('#students_names').append(new Option(data[1], data[0]))
}


function dataAnalysis(){
    $("#get_report_btn").addClass("loading disabled");
    var base = window.location.origin + '/hod/most_absentee';
    var course = $("#course").val()
    var year = $("#year").val()
    var data = JSON.stringify({"course": course,
                        "year": parseInt(year)})

    $.ajax({
        url: base,
        type: 'POST',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            $("#get_report_btn").removeClass("loading disabled");
            $("#which_class_head").html(course.toUpperCase()+" Year "+year+" Attendence Overview")
            $("#most_absentee_display").html(result)
            $("#attendOverview").show()
            $("#choose_detail").hide()
        },
        error: function(result){

            if(result.status == 406){
                $("#get_report_btn").removeClass("loading disabled");
                swal({
                    title: "Can't Analyze!",
                    text: "Maybe students not admitted or attendance not started taking.",
                    icon: "error",
                    button: "Okay!",
                })
            }
            else if(result.status == 404){
                $("#get_report_btn").removeClass("loading disabled");
                swal({
                    title: "Can't Analyze!",
                    text: "Check the duration of the course. Or contact the technical team.",
                    icon: "error",
                    button: "Okay!",
                })
            }
            else{
                $("#get_report_btn").removeClass("loading disabled");
                error_alert("Something went wrong please try to call the techinal team...")
            }

        }
    })
}


const month_names = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
'05': 'May', '06': 'June', '07': 'July', '08': 'August', 
'09': 'September', '10': 'October', '11': 'November', '12': 'December'}

function get_report(monthly = true){
    var base = window.location.origin + '/hod/get_report';
    var course = $("#course").val()
    var year = $("#year").val()

    if(monthly){
        $("#monthly_btn_report").addClass("loading disabled")
        var which_month = $("#datePicker").val().toString()
        var data = JSON.stringify({"course": course, "year": year,
                                    "last_month": monthly,
                                    "which_month": which_month})
        var report_head = month_names[which_month] + " Month Report"
    }
    else{
        $("#6_btn_report").addClass("loading disabled")
        var data = JSON.stringify({"course": course, "year": year,
                                    "last_month": monthly,
                                })
        var report_head = "6 Month Report"
    }

    $.ajax({
        url: base,
        type: 'POST',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            $("#report_table").html(result)
            $("#final_report_section").show()
            $("#final_report_head").html(report_head)
            $("#monthly_btn_report").removeClass("loading disabled")
            $("#6_btn_report").removeClass("loading disabled")

            $('html, body').animate({
                scrollTop: $("#final_report_head").offset().top
            }, 50);

        },
        error: function(result){

                if(result.status == 406){
                    $("#monthly_btn_report").removeClass("loading disabled")
                    $("#6_btn_report").removeClass("loading disabled")
                    swal({
                        title: "Can't Analyze!",
                        text: "Maybe students not admitted or attendance not started taking.",
                        icon: "error",
                        button: "Okay!",
                    })
                }
                else if(result.status == 404){
                    $("#monthly_btn_report").removeClass("loading disabled")
                    $("#6_btn_report").removeClass("loading disabled")
                    swal({
                        title: "Can't Analyze!",
                        text: "Check the duration of the course. Or contact the technical team.",
                        icon: "error",
                        button: "Okay!",
                    })
                }
                else{
                    $("#get_report_btn").removeClass("loading disabled");
                    error_alert("Something went wrong please try to call the techinal team...")
                }

        }
    });
}

function plot_pie(x, yValue){
    var xValues = ["Days(We Get)", "Days(Uoc)"]
    var barColors = ["#b91d47", "#00aba9"];
    var type = "pie"
    var data = {}
    new Chart("myChart", {
        type: "pie",
        data: {
            labels: xValues,
            datasets: [{
            backgroundColor: barColors,
            data: [x, yValue]
            }]
        },
    options: {
        title: {
                display: true,
                text: "Total Working Day Needed"
            },
        labels: {display: false}
        }
    })

}


function show_attendence(){
    var course = $("#course").val()
    var year = parseInt($("#year").val())
    var href = "/hod/students-attendence/"+course+"/"+year
    window.location.href = href
}

function show_details(who = "hod"){
    var course = $("#course").val()
    var year = parseInt($("#year").val())
    var href = "/"+who+"/students-attendence/details/"+course+"/"+year
    window.location.href = href
}

// student Search
$("#st_search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#report_table tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
  });


  function submit_correction(){
    var base = window.location.origin + '/hod/students-attendence/corrections';   
    var reason = $("#reason_attendence").val()
    var date = $("#date_giving").val()
    var students = $("#students_names").val()
    $("#sub_corr_btn").addClass("loading disabled")

    if (date && students != "" && reason != "") {
        var data = JSON.stringify({
                               "course": $("#course").val(),
                               "year": parseInt($("#year").val()),
                               "date": date.toString(),
                               "percentage": $("#percent").val(),
                               "names": students,
                               "reason":reason
                            });                    
        $.ajax({
            url: base,
            type: 'POST',
            async: true,
            data: data,
            dataType: 'json',
            contentType: "application/json",
            success: function(result){
                $("#sub_corr_btn").removeClass("loading disabled")
                swal({
                    title: "Attendence Updated!",
                    text: "Granded Attendence for Students",
                    icon: "success",
                    button: "Okay!",
                })
            },
            error: function(result){
                $("#sub_corr_btn").removeClass("loading disabled")
                if(result.status == 404){
                    swal({
                        title: "Attendence Not Taken!",
                        text: "In this date there is no attendence taken",
                        icon: "error",
                        button: "Okay!",
                    })
                }
                else{
                    error_alert("Something went wrong, please contact technical team")
                
                }
            }
        })
    }
    else{
        $("#sub_corr_btn").removeClass("loading disabled")
        warning_alert("Choose the date when you want to give attendance.")
    }
}

function get_studence_name(){
    $("#get_st_name_btn").addClass("loading disabled")
    var data = JSON.stringify({"course": $("#course").val(),
                               "year": parseInt($("#year").val()),
                               "date": '0000-00-00'
                            });
    
    var base = window.location.origin + '/attendence/set_class';   
    
    $.ajax({
        url: base,
        type: 'POST',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            $("#get_st_name_btn").removeClass("loading disabled")
            $("#students_name").empty()
            result.datas.forEach(append_student_name)
            swal({
                title: "Student Names Updated!",
                text: "Please choose students name.",
                icon: "success",
                button: "Okay!",
            })
        },
        error: function(result){
            $("#get_st_name_btn").removeClass("loading disabled")
            if(result.status == 404){
                swal({
                    title: "No Students!",
                    text: "There is no student admitted in this course.",
                    icon: "error",
                    button: "Okay!",
                })
            }
            else if(result.status == 406){
                var msg = JSON.parse(result.responseText)
                swal({
                    title: "Already taken!",
                    text: msg.detail,
                    icon: "error",
                    button: "Okay!",
                })
            }
            else{
                error_alert("Something went wrong please try to call the techinal team...")
            }
        }

    })
}
