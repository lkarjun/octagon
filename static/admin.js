// Department remove
function remove_departement(id){
    base = window.location.origin + '/admin/portal/deletedepartment';
    data = JSON.stringify({"department": id});
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