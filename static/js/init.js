(function($){
  $(function(){

    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    
  }); // end of document ready
})(jQuery); // end of jQuery name space

$(document).ready(function(){

  $('#modal1').modal({
    dismissible: true, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    in_duration: 300, // Transition in duration
    out_duration: 200, // Transition out duration
    starting_top: '4%', // Starting top style attribute
    ending_top: '10%', // Ending top style attribute
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        $('#modal2').modal('close');
        $('#modal3').modal('close');
        console.log(modal, trigger);
      }
  }
  );

  $('#modal2').modal({
    dismissible: true, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    in_duration: 300, // Transition in duration
    out_duration: 200, // Transition out duration
    starting_top: '4%', // Starting top style attribute
    ending_top: '10%', // Ending top style attribute
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        $('#modal1').modal('close');
        $('#modal3').modal('close');
        console.log(modal, trigger);
      }
  }
  );

  $('#modal3').modal({
    dismissible: true, // Modal can be dismissed by clicking outside of the modal
    opacity: .5, // Opacity of modal background
    in_duration: 300, // Transition in duration
    out_duration: 200, // Transition out duration
    starting_top: '4%', // Starting top style attribute
    ending_top: '10%', // Ending top style attribute
    ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        $('#modal1').modal('close');
        $('#modal2').modal('close');
        console.log(modal, trigger);
      }
  }
  );

  $(".dropdown-button").dropdown();

});

