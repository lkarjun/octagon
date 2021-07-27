// Department remove
function remove_departement(id){
    var base = window.location.origin + '/admin/portal/deletedepartment';
    var data = JSON.stringify({"department": id});
    $.ajax({
          url: base,
          type: 'DELETE',
          async: true,
          data: data,
          dataType: 'json',
          contentType: "application/json",

          success: function(result) {
            $('#'+id).remove();
            success_alert('Successfully Removed Department: '+id);
            },
          error: function(result){
            error_alert('Something Went Wrong Error: '+result);
          }
      });
}

// Add Department
$("#Department_form").submit((e)=>{
  e.preventDefault()
  var base = window.location.origin + '/admin/portal/Adddepartment';
  var department = $("#dep_name").val()
  var alias = $('#dep_alias').val()
  var data = JSON.stringify({"Department": department, "Alias": alias})        
  $.ajax({
    url: base,
    type: 'POST',
    async: true,
    data: data,
    dataType: 'json',
    contentType: "application/json",

    success: function(result) {
      success_alert('Successfully Added Department: '+department);
      $("#Department_form")[0].reset()
      },
    error: function(result){
      error_alert("Error, we won't allow duplicate entries...");
    }
  });

});

// Remove Course

$("#Course_Remove_form").submit((e)=>{
  e.preventDefault()
  var base = window.location.origin + '/admin/portal/deletecourse';
  var name = $("#course_options").val()
  if (name == 'none'){warning_alert("Please choose valid course name...");}
  else{
    var data = JSON.stringify({"course_name": name})   

    $.ajax({
      url: base,
      type: 'DELETE',
      async: true,
      data: data,
      dataType: 'json',
      contentType: "application/json",

      success: function(result) {
          var opt = "#course_options option[value='"+name+"']"
          success_alert('Successfully Removed Course: '+name);
          $(opt).remove();
        },
      error: function(result){
          error_alert("Something Went Wrong. Please try to contact the techincal team...");
        }
      });
    }
});

// Add Course

$("#Course_form").submit((e)=>{
  e.preventDefault()
  var base = window.location.origin + '/admin/portal/AddCourse';
  var names = $("#course_name").val()
  var alias = $('#course_shortform').val()
  var duration = $('#course_duration').val()
  var department = $('#department_options3').val()
  var data = JSON.stringify({"course_name": names, "course_alias": alias, "duration": duration, "department": department})   
  
  $.ajax({
    url: base,
    type: 'POST',
    async: true,
    data: data,
    dataType: 'json',
    contentType: "application/json",

    success: function(result) {
        success_alert('Successfully Added Course: '+names);
        $("#Course_form")[0].reset()
        $('#course_options').append("<option value="+alias+">"+names+"</option>")
      },
    error: function(result){
        error_alert("Error, we won't allow duplicate entries...");
      }
    });
})


// Remove Hod

$("#Hod_remove").submit((e)=>{
  e.preventDefault()
  var base = window.location.origin + '/admin/portal/delete_hod';
  var names = $("#hod_name").val()
  var dep = $('#department_options2').val()
  if (names == "none"){warning_alert("Please choose valid hod name")}
  else{
    var data = JSON.stringify({"name": names, "department": dep})

    $.ajax({
      url: base,
      type: 'DELETE',
      async: true,
      data: data,
      dataType: 'json',
      contentType: "application/json",

      success: function(result) {
            var opt = "#hod_name option[value='"+names+"']";
            success_alert('Successfully Removed Hod: '+names);
            $(opt).remove();
          },
      error: function(result){
            error_alert("Something Went Wrong. Please try to contact the techincal team...");
          }
      });
  }
})


// Appointment of hod and Verification image sends

function appoint_hod(data, name, username){
  console.log(data)
  var base = window.location.origin + '/admin/portal/create_hod';
  $.ajax({
        url: base,
        type: 'POST',
        async: true,
        data: data,
        dataType: 'json',
        contentType: "application/json",

        success: function(result) {
            success_alert('Successfully Appointed '+name+' as new hod');
            $("#upload_button").removeClass("loading disabled");
        },
        error: function(result){
            if(result.status == 406){
              var message = JSON.parse(result.responseText)
              warning_alert(message.detail)
              $("#upload_button").removeClass("loading disabled");
            }
            else{
              error_alert("Something Went Wrong. Please try to contact the techincal team...");
            }
          }
        });

}

function verification_image_upload(data, name, user_name){
  var base = window.location.origin + '/admin/portal/verification_image';
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
      appoint_hod(data, name, user_name)
    },
    error: function(result){
      error_alert("Something Went Wrong. Please try to contact the techincal team...");
    }
  })
}

$("#Appointment_form").submit((e)=>{
  e.preventDefault();
  var name = $('#name').val()
  var email = $('#email').val()
  var phone = parseInt($('#number').val())
  var username = $('#username').val()
  var department = $('#department_options').val()
  var data = JSON.stringify({"name": name, "email": email, "phone_num": phone, "user_name": username, "department": department})
  $("#upload_button").addClass("loading disabled");
  verification_image_upload(data, name, username)
})


// Admin password change...
$("#admin_reset").submit((e)=>{
  e.preventDefault()
  var base = window.location.origin + '/admin/portal/reset_password';
  var data = JSON.stringify({"current_pass": $('#inputPassword').val(), "new_pass": $("#inputPasswordNew").val()})
  $("#pass_change_button").addClass("loading disabled");
  $.ajax({
    url: base,
    type: 'POST',
    async: true,
    data: data,
    dataType: 'json',
    contentType: "application/json",
    success: function(result){
      $("#pass_change_button").removeClass("loading disabled");
      success_alert(result)
      $("#admin_reset")[0].reset()
    },
    error: function(result){
      $("#pass_change_button").removeClass("loading disabled");
      if(result.status == 406){
        var message = JSON.parse(result.responseText)
        warning_alert(message.detail);
        $("#admin_reset")[0].reset()
      }
      else{
        error_alert("Something Went Wrong. Please try to contact the techincal team...");
        location.reload();
      }
    }

  })
});