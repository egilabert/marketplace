(function($){
  $(function(){

    $( "#client_form" ).click(function(e) {
      e.preventDefault();
      form_filled_check = true;
      $('.ajax_bar').show();
      var sector = $("#autocomplete-input").val();
      var region = $("#region_checkbox").is(":checked");
      var min_bill = $("#test5").val();
      var comment = $("#comment_textarea").val();

      $.ajax({
        url: '/empresas/clients/',
        type: 'get',
        data:{ sector: sector, region : region, min_bill: min_bill, comment: comment}})
          .done( function (responseText) {
                  // Triggered if response status code is 200 (OK)
                  $('#cards_container').html(responseText);
                  $('#modal_clients').modal('close');
               })
               .fail( function (jqXHR, status, error) {
                  // Triggered if response status code is NOT 200 (OK)
                  console.log(error)
                  alert(jqXHR.responseText);
               })
               .always( function() {
                  // Always run after .done() or .fail()
                  $('.ajax_bar').hide();
               });

    });
    

    $('#loadingmessage').hide();
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $(".dropdown-button").dropdown();
    $('#hamb').sideNav();
    
    
    $('.modal').modal({
      opacity: .5, // Opacity of modal background
      in_duration: 300, // Transition in duration
      out_duration: 200, // Transition out duration
      starting_top: '4%', // Starting top style attribute
      ending_top: '5%', // Ending top style attribute
    });
    $('select').material_select();
    
    //Abril el formulario de filtros de clientes recommendados
    
    $('.client_form_button').click(function() {
      $('#modal_clients').modal('open');
    });

    $('.ajax_bar').hide();
      
    $('input.autocomplete').autocomplete({
      data: {
        "Otros servicios personales": null,
        "Edición": null,
        "Actividades de organizaciones y organismos extraterritoriales": null,
        "Comercio al por mayor e intermediarios del comercio, excepto de vehículos de motor y motocicletas": null,
        "Industria de la alimentación": null,
        "Comercio al por menor, excepto de vehículos de motor y motocicletas": null,
        "Actividades inmobiliarias": null,
        "Industria del cuero y del calzado": null,
        "Otras actividades profesionales, científicas y técnicas": null,
        "Agricultura, ganadería, caza y servicios relacionados con las mismas": null,
        "Ingeniería civil": null,
        "Fabricación de otros productos minerales no metálicos": null,
        "Servicios de información": null,
        "Construcción de edificios": null,
        "Fabricación de bebidas": null,
        "Industria textil": null,
        "Fabricación de productos de caucho y plásticos": null,
        "Fabricación de maquinaria y equipo n.c.o.p.": null,
        "Fabricación de material y equipo eléctrico": null,
        "Actividades cinematográficas, de vídeo y de programas de televisión, grabación de sonido y edición musical": null,
        "Artes gráficas y reproducción de soportes grabados": null,
        "Confección de prendas de vestir": null,
        "Fabricación de productos metálicos, excepto maquinaria y equipo": null,
        "Venta y reparación de vehículos de motor y motocicletas": null,
        "Actividades administrativas de oficina y otras actividades auxiliares a las empresas": null,
        "Otras industrias manufactureras": null,
        "Industria química": null,
        "Actividades de alquiler": null,
        "Actividades deportivas, recreativas y de entretenimiento": null,
        "Actividades de construcción especializada": null,
        "Metalurgia; fabricación de productos de hierro, acero y ferroaleaciones": null,
        "Industria del papel": null,
        "Servicios técnicos de arquitectura e ingeniería; ensayos y análisis técnicos": null,
        "Fabricación de vehículos de motor, remolques y semirremolques": null,
        "Fabricación de muebles": null,
        "Actividades de agencias de viajes, operadores turísticos, servicios de reservas y actividades relacionadas con los mismos": null,
        "Recogida y tratamiento de aguas residuales": null,
        "Actividades de las sedes centrales; actividades de consultoría de gestión empresarial": null,
        "Reparación e instalación de maquinaria y equipo": null,
        "Programación, consultoría y otras actividades relacionadas con la informática": null,
        "Fabricación de productos informáticos, electrónicos y ópticos": null,
        "Transporte terrestre y por tubería": null,
        "Industria de la madera y del corcho, excepto muebles; cestería y espartería": null,
        "Otras industrias extractivas": null,
        "Suministro de energía eléctrica, gas, vapor y aire acondicionado": null,
        "Servicios de alojamiento": null,
        "Extracción de minerales metálicos": null,
        "Investigación y desarrollo": null,
        "Actividades sanitarias": null,
        "Actividades jurídicas y de contabilidad": null,
        "Publicidad y estudios de mercado": null,
        "Actividades de juegos de azar y apuestas": null,
        "Actividades de seguridad e investigación": null,
        "Administración Pública y defensa; Seguridad Social obligatoria": null,
        "Asistencia en establecimientos residenciales": null,
        "Servicios de comidas y bebidas": null,
        "Almacenamiento y actividades anexas al transporte": null,
        "Reparación de ordenadores, efectos personales y artículos de uso doméstico": null,
        "Actividades asociativas": null,
        "Recogida, tratamiento y eliminación de residuos; valorización": null,
        "Servicios financieros, excepto seguros y fondos de pensiones": null,
        "Actividades auxiliares a los servicios financieros y a los seguros": null,
        "Educación": null,
        "Extracción de antracita, hulla y lignito": null,
        "Telecomunicaciones": null,
        "Actividades de creación, artísticas y espectáculos": null,
        "Fabricación de productos farmacéuticos": null,
        "Pesca y acuicultura": null,
        "Actividades relacionadas con el empleo": null,
        "Servicios a edificios y actividades de jardinería": null,
        "Actividades postales y de correos": null,
        "Actividades de servicios sociales sin alojamiento": null,
        "Transporte marítimo y por vías navegables interiores": null,
        "Actividades de los hogares como productores de bienes y servicios para uso propio": null,
        "Transporte aéreo": null,
        "Fabricación de otro material de transporte": null,
        "Actividades de programación y emisión de radio y televisión": null,
        "Captación, depuración y distribución de agua": null,
        "Actividades de bibliotecas, archivos, museos y otras actividades culturales": null,
        "Actividades de descontaminación y otros servicios de gestión de residuos": null,
        "Actividades veterinarias": null,
        "Actividades de los hogares como empleadores de personal doméstico": null,
        "Apple": null,
        "Microsoft": null,
        "Google": 'http://placehold.it/250x250'
      }
    });

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
    
    $('a').click(function(){
        $('html, body').animate({
            scrollTop: $( $(this).attr('href') ).offset()
        }, 1000);
        return false;
    });

    //entrada en tempos de en la landing de la Network B2B
    // $( ".fadding" ).fadeIn( 1500, function() {
    //   $( ".fadding_2" ).fadeIn( 700, function() {
    //     $( ".fadding_3" ).fadeIn( "slow", function() {
    //     });
    //   });
    // });
    
  }); // end of document ready
})(jQuery); // end of jQuery name space