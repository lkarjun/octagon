//Verification Image Upload

function verification_image_upload(data, user_name, name){
    var base = window.location.origin + '/hod/verification_image';
    var form_data = new FormData()
    form_data.append('username', user_name);
    form_data.append('image1', $('#vimage1')[0].files[0])
    form_data.append('image2', $('#vimage2')[0].files[0])
    form_data.append('image3', $('#vimage3')[0].files[0])
    console.log(form_data)
  
    $.ajax({
      url: base,
      type: 'POST',
      async: true,
      data: form_data,
      cache: false,
      
      contentType: false,
      processData: false,
      success: function(result){
        console.log("Verification Images uploaded");
        appoint_teacher(data, name)
      },
      error: function(result){
        error_alert("Something Went Wrong. Please try to contact the techincal team...");
      }
    })
}

// Appoint Teacher

function appoint_teacher(data, name){
    var base = window.location.origin + '/hod/Addteacher';
    
    $.ajax({
      
      url: base,
      type: 'POST',
      data: data,
      dataType: 'json',
      contentType: "application/json",
      success: function(result){
        $("#appoint_btn").removeClass("loading")
      
        swal({
              title: "Appointed Teacher!",
              text: "Sucessfully Appointed Teacher " + name,
              icon: "success",
              button: "Okay!",
          }).then((value) => {
                location.reload();
                });


      },
      error: function(result){
        $("#appoint_btn").removeClass("loading")
        error_alert("Something Went Wrong. Please try to contact the techincal team...");
      }
     
    })
}

$("#Appointment_form").submit((e)=>{
    e.preventDefault()
    $("#appoint_btn").addClass("loading")

    var base = window.location.origin + '/hod/Addteacher';

    var name = $("#name").val()
    var email = $("#email").val()
    var username = $("#username").val()
    var phone_number = parseInt($("#number").val())
    var tag = $("#tag").val()
    var depart = $("#depart").val()
    var data = JSON.stringify({"name": name, "username": username, "department": depart,
                "email": email, "phone_number": phone_number, "tag": tag})
    
    verification_image_upload(data, username, name)
  })


  // Teacher Search
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Teachers tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });


  // Remove Teacher
  function remove_teacher(username, name){
    var base = window.location.origin + '/hod/Deleteteacher';
    var data = JSON.stringify({"name": name, "user_name": username});
    $.ajax({
      url: base,
      type: 'DELETE',
      async: true,
      data: data,
      dataType: 'json',
      contentType: "application/json",

      success: function(result) {
        $('#'+username).remove();
        success_alert('Successfully Removed Teacher: '+name);
        },
      error: function(result){
        error_alert('Something Went Wrong Error: '+result);
        }
      });
    }