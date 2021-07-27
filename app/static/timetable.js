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