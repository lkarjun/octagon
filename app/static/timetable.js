function clone_it(){
    $('#mt1 option').clone().appendTo('#mt2');
    $('#mt1 option').clone().appendTo('#mt3');
    $('#mt1 option').clone().appendTo('#mt4');
    $('#mt1 option').clone().appendTo('#mt5');
    $('#mt1 option').clone().appendTo('#tt1');
    $('#mt1 option').clone().appendTo('#tt2');
    $('#mt1 option').clone().appendTo('#tt3');
    $('#mt1 option').clone().appendTo('#tt4');
    $('#mt1 option').clone().appendTo('#tt5');
    $('#mt1 option').clone().appendTo('#wt1');
    $('#mt1 option').clone().appendTo('#wt2');
    $('#mt1 option').clone().appendTo('#wt3');
    $('#mt1 option').clone().appendTo('#wt4');
    $('#mt1 option').clone().appendTo('#wt5');
    $('#mt1 option').clone().appendTo('#tut1');
    $('#mt1 option').clone().appendTo('#tut2');
    $('#mt1 option').clone().appendTo('#tut3');
    $('#mt1 option').clone().appendTo('#tut4');
    $('#mt1 option').clone().appendTo('#tut5');
    $('#mt1 option').clone().appendTo('#ft1');
    $('#mt1 option').clone().appendTo('#ft2');
    $('#mt1 option').clone().appendTo('#ft3');
    $('#mt1 option').clone().appendTo('#ft4');
    $('#mt1 option').clone().appendTo('#ft5');
}

function get_hour_day(id){
    const dayHour = {
                        "#mt1": ["Monday", "hour_1"],
                        "#mt2": ["Monday", "hour_2"],
                        "#mt3": ["Monday", "hour_3"],
                        "#mt4": ["Monday", "hour_4"],
                        "#mt5": ["Monday", "hour_5"],
                        "#tt1": ["Tuesday", "hour_1"],
                        "#tt2": ["Tuesday", "hour_2"],
                        "#tt3": ["Tuesday", "hour_3"],
                        "#tt4": ["Tuesday", "hour_4"],
                        "#tt5": ["Tuesday", "hour_5"],
                        "#wt1": ["Wednesday", "hour_1"],
                        "#wt2": ["Wednesday", "hour_2"],
                        "#wt3": ["Wednesday", "hour_3"],
                        "#wt4": ["Wednesday", "hour_4"],
                        "#wt5": ["Wednesday", "hour_5"],
                        "#tut1": ["Thursday", "hour_1"],
                        "#tut2": ["Thursday", "hour_2"],
                        "#tut3": ["Thursday", "hour_3"],
                        "#tut4": ["Thursday", "hour_4"],
                        "#tut5": ["Thursday", "hour_5"],
                        "#ft1": ["Friday", "hour_1"],
                        "#ft2": ["Friday", "hour_2"],
                        "#ft3": ["Friday", "hour_3"],
                        "#ft4": ["Friday", "hour_4"],
                        "#ft5": ["Friday", "hour_5"],
                    }
    return dayHour[id]
}

var countValidity = 0

function checkConflict(id){
    value = $(id).val()
    data = get_hour_day(id)
    data = JSON.stringify({"day": data[0], "name": value, "hour": data[1]})
    
    if (value == "none"){
        $(id+"f").addClass("error");
        warning_alert('Choose a valid name '+value);   
    }
    else{
        var base = window.location.origin + '/hod/check_teacher';            
        $.ajax({
                url: base,
                type: 'POST',
                async: true,
                data: data,
                dataType: 'json',
                contentType: "application/json",
                success: function(result){
                    console.log(result)
                    $(id+"f").removeClass("error").addClass("disabled")
                    countValidity += 1;
                    if(countValidity == 25){
                        $("#finalize").removeClass("disabled")
                        countValidity = 0;
                    }
                },
                error: function(result){
                        
                        if(result.status == 406){
                            msg = JSON.parse(result.responseText)
                            error_alert(msg.detail)
                            $(id+"f").addClass("error")
                        }
                        else{
                            error_alert("Something went wrong please contact techincal team...");
                        }
                    }
            });
    }
    
}


$("#CourseAndYear").submit((e)=>{
    e.preventDefault()

    $("#finalize").addClass("loading")
    var depart = $("#department").val()
    var course = $("#course").val()
    var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    var year = parseInt($("#year").val())
    var day_1 = [$("#mt1").val(), $("#mt2").val(), $("#mt3").val(), $("#mt4").val(), $("#mt5").val()]
    var day_2 = [$("#tt1").val(), $("#tt2").val(), $("#tt3").val(), $("#tt4").val(), $("#tt5").val()]
    var day_3 = [$("#wt1").val(), $("#wt2").val(), $("#wt3").val(), $("#wt4").val(), $("#wt5").val()]
    var day_4 = [$("#tut1").val(), $("#tut2").val(), $("#tut3").val(), $("#tut4").val(), $("#tut5").val()]
    var day_5 = [$("#ft1").val(), $("#ft2").val(), $("#ft3").val(), $("#ft4").val(), $("#ft5").val()]
    var data = JSON.stringify({"department": depart, "course": course, "year": year,
                                "day_1": day_1, "day_2": day_2, "day_3": day_3, "day_4": day_4,
                                "day_5": day_5})

    var base = window.location.origin + '/hod/CreateTimeTable';
    $.ajax({
            url: base,
            type: 'POST',
            async: true,
            data: data,
            dataType: 'json',
            contentType: "application/json",
            success: function(result){
                    var msg = "Succesfully created new timetable for "+course+" year"+year
                    $("#finalize").removeClass("loading")
                    swal({
                        title: "Time Table Created!",
                        text: msg,
                        icon: "success",
                        button: "Okay!",
                      }).then((value) => {
                          location.reload();
                        });
                    },
             error: function(result){
                    $("#finalize").removeClass("loading")
                        if(result.status == 422){
                            warning_alert("Please fill all necessary columns...")
                        }
                        else{
                            error_alert("Something went wrong please try to contact techinal team...")
                            }
                        }
    });
})


$("#RemoveTT").submit((e)=>{
    e.preventDefault()
    var course = $("#courseR").val()
    var year = parseInt($("#yearR").val())
    var depart = $("#departR").val()
    var data = JSON.stringify({"course": course, "year": year, "department": depart})

    var base = window.location.origin + '/hod/delete_timetable';
    $.ajax({
        url: base,
        type: 'DELETE',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            swal({
                    title: "Removed!",
                    text: "Removed Time Table "+course+" year "+year,
                    icon: "success",
                    button: "Okay!",
                })
                
        },
        error: function(result){
            if(result.status == 404){
                var msg = JSON.parse(result.responseText)
                swal({
                        title: "Not Removed!",
                        text: msg.detail,
                        icon: "error",
                        button: "Okay!",
                    })
            }
            else{
                error_alert("Something went wrong please try to call the techinal team...")
            }
        }
    });
})


function setTimeTable(data, result){
    var Monday = result['Monday']
    var Tuesday = result['Tuesday']
    var Wednesday = result['Wednesday']
    var Thursday = result['Thursday']
    var Friday = result['Friday']
    $("#viewTTData").show()
    $("#headTimeTableCourse").html(data)
    // monday
    $("#vm1").html(Monday[0])
    $("#vm2").html(Monday[1])
    $("#vm3").html(Monday[2])
    $("#vm4").html(Monday[3])
    $("#vm5").html(Monday[4])
    // tuesday
    $("#vt1").html(Tuesday[0])
    $("#vt2").html(Tuesday[1])
    $("#vt3").html(Tuesday[2])
    $("#vt4").html(Tuesday[3])
    $("#vt5").html(Tuesday[4])
    // wednesday
    $("#vw1").html(Wednesday[0])
    $("#vw2").html(Wednesday[1])
    $("#vw3").html(Wednesday[2])
    $("#vw4").html(Wednesday[3])
    $("#vw5").html(Wednesday[4])
    // thursday
    $("#vth1").html(Thursday[0])
    $("#vth2").html(Thursday[1])
    $("#vth3").html(Thursday[2])
    $("#vth4").html(Thursday[3])
    $("#vth5").html(Thursday[4])
    // tuesday
    $("#vf1").html(Friday[0])
    $("#vf2").html(Friday[1])
    $("#vf3").html(Friday[2])
    $("#vf4").html(Friday[3])
    $("#vf5").html(Friday[4])
}

$("#viewTT").submit((e)=>{
    e.preventDefault()
    var course = $("#courseV").val()
    var year = parseInt($("#yearV").val())
    var depart = $("#departV").val()
    var data = JSON.stringify({"course": course, "year": year, "department": depart})

    var base = window.location.origin + '/hod/display_timetable';
    $.ajax({
        url: base,
        type: 'POST',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            var data = course+" "+year+" year"
            setTimeTable(data, result)
        },
    error: function(result){
        error_alert("Something went wrong please try to call the techinal team...")
        }
    });
})