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
            }
            else{
                error_alert("Something Went Wrong. Please try to contact the techincal team...");
            }
        }
    })

})
