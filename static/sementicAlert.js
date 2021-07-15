$.uiAlert = function(options) {
    var setUI = $.extend({
      text: 'You may now log-in with the username you have chosen',
      textcolor: '#19c3aa',
      bgcolors: '#fff',
      position: 'top-right',
      icon: '',
      time: 5,
      permanent: false
    }, options);
  
      var ui_alert = 'ui-alert-content';
        ui_alert += '-' + setUI.position;
        setUI.bgcolors ='style="background-color: '+setUI.bgcolor+';   box-shadow: 0 0 0 1px rgba(255,255,255,.5) inset,0 0 0 0 transparent;"';
        if(setUI.bgcolors === '') setUI.bgcolors ='style="background-color: ; box-shadow: 0 0 0 1px rgba(255,255,255,.5) inset,0 0 0 0 transparent;"';
      if(!$('body > .' + ui_alert).length) {
        $('body').append('<div class="ui-alert-content ' + ui_alert + '" style="width: inherit;"></div>');
      }
      var message = $('<div id="messages" class="ui icon message" ' + setUI.bgcolors + '></i><i class="close icon" style="color: '+setUI.textcolor+';" id="messageclose"></i><div style="color: '+setUI.textcolor+'; margin-right: 10px;">   <div class="header">'+setUI.text+'</div> </div>  </div>');
      $('.' + ui_alert).prepend(message);
      message.animate({
        opacity: '1',
      }, 300);
      if(setUI.permanent === false){
        var timer = 0;
        $(message).mouseenter(function(){
          clearTimeout(timer);
        }).mouseleave(function(){
          uiAlertHide();
        });
        uiAlertHide();
      }
      function uiAlertHide(){
        timer = setTimeout(function() {
          message.animate({
            opacity: '0',
          }, 300, function() {
            message.remove();
          });
        }, (setUI.time * 1000) );
      }
  
      $('#messageclose')
      .on('click', function() {
        $(this)
          .closest('#messages')
          .transition('fade')
        ;
      })
    ;
  
    };

  
// Success alert
function success_alert(text, position = 'bottom-right'){
    $.uiAlert({
    text: text,
    bgcolor: '#00B74A',
    textcolor: '#FBFBFB',
    position: position,
    time: 3,
  })
};

// Error alert
function error_alert(text, position = 'bottom-right'){
    $.uiAlert({
      text: text,
      bgcolor: '#F93154',
      textcolor: '#FBFBFB',
      position: position,
      time: 3,
    })
}

// Warning Alert
function warning_alert(text, position = 'bottom-right'){
  $.uiAlert({
    text: text,
    bgcolor: '#FFA900',
    textcolor: '#FBFBFB',
    position: position,
    time: 3,
  })
}