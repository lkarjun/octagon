$("#NewStudent").submit((e)=>{
    e.preventDefault()
    $("#appoint_btn").addClass("loading");
    var name = $("#name").val()
    var data = JSON.stringify({"unique_id": $("#unique_id").val(), "name": name,
                 "email": $("#email").val(), "parent_name": $("#parent_name").val(),
                 "parent_number": $("#parent_number").val(), "number": $("#number").val(),
                 "course": $("#course").val(), "year": $("#year").val()});
    
    var base = window.location.origin + '/teacher/add-students';

    $.ajax({

        url: base,
        type: 'POST',
        data: data,
        dataType: 'json',
        contentType: "application/json",
        
        success: function(result){
            $("#appoint_btn").removeClass("loading");
            swal({
                title: "Added Student!",
                text: "Sucessfully Added Student: " + name,
                icon: "success",
                button: "Okay!",
            }).then((value) => {location.reload();});
        },
        error: function(result){
            $("#appoint_btn").removeClass("loading")
            error_alert("Something Went Wrong. Please try to contact the techincal team...");
        }

    })
})


$("#removeStudent").submit((e)=>{
    e.preventDefault();
    $("#appoint_btn1").addClass("loading disabled");
    var name = $("#rmName").val()
    var data = JSON.stringify(
                {"unique_id": $("#id1").val(), "name": name,
                "course": $("#course1").val(), "year": parseInt($("#year1").val())}
            );
    var base = window.location.origin + '/teacher/delete-student';

    $.ajax({

        url: base,
        type: 'DELETE',
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){

            $("#appoint_btn1").removeClass("loading disabled");
            swal({
                title: "Removed Student!",
                text: "Sucessfully Remove Student: " + name,
                icon: "success",
                button: "Okay!",
            }).then((value) => {location.reload();});
        
        },
        error: function(result){
            if(result.status == 404){
                swal({
                    title: "Not Found!",
                    text: name + "not found in database",
                    icon: "error",
                    button: "Okay!",
                })
                $("#appoint_btn1").removeClass("loading disabled");
            }
            else{
                $("#appoint_btn1").removeClass("loading disabled");
                error_alert("Something Went Wrong. Please try to contact the techincal team...");
            }
        }
    })

})


function reset_edit(){
    $("#editVerify")[0].reset();
    $("#appoint_btn2").removeClass("disabled")
    $("#editstudent")[0].reset()
    $(".edbtndis").addClass("disabled")
}


$("#editVerify").submit((e)=>{
    e.preventDefault();
    $("#appoint_btn2").addClass("loading disabled");
    var name = $("#edName").val()
    var data = JSON.stringify(
        {"unique_id": $("#id2").val(), "name": name,
        "course": $("#edCourse1").val(), "year": parseInt($("#edYear1").val())}
    );
    
    var base = window.location.origin + '/teacher/edit-student';

    $.ajax({

        url: base,
        type: 'POST',
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            $("#appoint_btn2").removeClass("loading disabled");
            $("#appoint_btn2").addClass("disabled")
            set_details(result)
            console.log(result)
        },
        error: function(result){
            $("#appoint_btn2").removeClass("loading disabled");
            if(result.status == 404){
                swal({
                    title: "Not Found!",
                    text: name + "details not found in database",
                    icon: "error",
                    button: "Okay!",
                })
            }
            else{
                error_alert("Something Went Wrong. Please try to contact the techincal team...");
            }
        }
    })
})


function set_details(data){
    console.log(data.name)
    $("#id4").val(data.unique_id)
    $("#name4").val(data.name)
    $("#email4").val(data.email)
    $("#pname4").val(data.parent_name)
    $("#pnumber4").val(data.parent_number)
    $("#snumber4").val(data.number)
    $("#course4").val(data.course).change()
    $("#year4").val(data.year).change()
    $(".edbtndis").removeClass("disabled")
}


$("#editstudent").submit((e)=>{
    e.preventDefault();

    $("#appoint_btn_ed").addClass("loading disabled");
    var name = $("#name4").val()
    var data = JSON.stringify(
                {"unique_id": $("#id4").val(), "name": name,
                "email": $("#email4").val(), "parent_name": $("#pname4").val(),
                "parent_number": $("#pnumber4").val(), "number": $("#snumber4").val(),
                "course": $("#course4").val(), "year": $("#year4").val(),
                "old_unique_id": $("#id2").val(), "old_name": $("#edName").val(),
                "old_course": $("#edCourse1").val(), "old_year": parseInt($("#edYear1").val())}
                );

    var base = window.location.origin + '/teacher/edit-student';

    $.ajax({

        url: base,
        type: 'PUT',
        data: data,
        dataType: 'json',
        contentType: "application/json",
        success: function(result){
            $("#appoint_btn_ed").removeClass("loading disabled");
            swal({
                title: "Updated Student Details!",
                text: "Sucessfully Updated Student: " + name,
                icon: "success",
                button: "Okay!",
            }).then((value) => {location.reload();});
        },
        error: function(result){
            $("#appoint_btn_ed").removeClass("loading disabled");
            if(result.status == 404){
                swal({
                    title: "Not Found!",
                    text: name + "details not found in database",
                    icon: "error",
                    button: "Okay!",
                })
            }
            else{
                error_alert("Something Went Wrong. Please try to contact the techincal team...");
            }
        }
    })
})
