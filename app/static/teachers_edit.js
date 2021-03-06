//Verification Image Upload

function verification_image_upload(data, username, name){
  var base = window.location.origin + '/hod/verification_image';
  var form_data = new FormData()
  form_data.append('username', username);
  form_data.append('image1', $('#vimage1')[0].files[0])
  form_data.append('image2', $('#vimage2')[0].files[0])
  form_data.append('image3', $('#vimage3')[0].files[0])
  console.log(form_data)

  $("#pro").show()
  $.ajax({
    xhr: function() {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function(evt) {
          if (evt.lengthComputable) {
              var percentComplete = Math.round((evt.loaded / evt.total) * 100);
              $(".progress-bar").width(percentComplete + '%');
              $(".progress-bar").html(percentComplete+'%');
          }
      }, false);
      return xhr;
    },
    url: base,
    type: 'POST',
    async: true,
    data: form_data,
    cache: false,
    
    contentType: false,
    processData: false,
    beforeSend: function(){
      $(".progress-bar").width('0%');
      $('#uploadStatus').html('<img src="images/loading.gif"/>');
    },
    success: function(result){
      console.log("Verification Images uploaded");
      appoint_teacher(data, name)
      $("#pro").hide()
    },
    error: function(result){
      if(result.status == 415){
        $("#appoint_btn").removeClass("loading disabled")
        $("#pro").hide()
        swal({
          text: "Please retake image...",
          icon: "warning",
          button: "Okay"
        })
      }
      else{
        $("#pro").hide()
        swal({
            text: "Something Went Wrong. Please try to contact the techincal team...",
            icon: "error",
            button: "Okay"  
          }).then((value) => {
            location.reload();
          })   
      }
      
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
      $("#appoint_btn").removeClass("loading disabled")
      $("#pro").hide()
      swal({
            title: "Appointed Teacher!",
            text: "Sucessfully Appointed Teacher " + name,
            icon: "success",
            button: "Okay!",
        })
    },
    error: function(result){
      $("#pro").hide()
      $("#appoint_btn").removeClass("loading disabled")
      swal({
            text: "Something Went Wrong. Please try to contact the techincal team...",
            icon: "error",
            button: "Okay"  
          }).then((value) => {
            location.reload();
          })
    }
   
  })
}

$("#Appointment_form").submit((e)=>{
  e.preventDefault()
  $("#appoint_btn").addClass("loading disabled")

  var base = window.location.origin + '/hod/Addteacher';

  var name = $("#name").val()
  var email = $("#email").val()
  var phone_num = parseInt($("#number").val())
  var username = $("#username").val()
  var username = name.replaceAll(/\s/g,'').toLowerCase().slice(0,3) + String(phone_num).slice(7) + username
  var tag = $("#tag").val()
  var depart = $("#depart").val()
  var data = JSON.stringify({"name": name, "username": username, "department": depart,
              "email": email, "phone_num": phone_num, "tag": tag})
  
  appoint_teacher(data, name)
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
    $("#"+username).addClass("bg-danger")
    var base = window.location.origin + '/hod/Deleteteacher';
    var data = JSON.stringify({"name": name, "username": username});
    $.ajax({
      url: base,
      type: 'DELETE',
      async: true,
      data: data,
      dataType: 'json',
      contentType: "application/json",

      success: function(result) {
        $('#'+username).remove();
        swal({
          text: 'Successfully Removed Teacher: '+name,
          icon: 'success',
          button: 'Okay'
        });
        },
      error: function(result){
        $("#"+username).removeClass("bg-danger")
        $("#"+username).addClass("bg-warning")
        swal({
          text: 'Something Went Wrong Error: '+result,
          icon: "error",
          button: "Okay"
        })
        }
      });
    }