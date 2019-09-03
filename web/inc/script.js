$(function() {

  var zoom_graph = 8;
  var zoom_graph_colors = 2;
  var scan_interval = 2000;

  // ON CHANGE
  $('.col input[type="number"]').change(function(){
    var is_color = $(this).parent().parent().hasClass('com');
    var zoom_to_use = is_color ? zoom_graph_colors : zoom_graph;
    var width = $(this).val() * zoom_to_use;
    $(this).parent().find('.bar').width(width + 'px');
    if( $(this).parent().parent().parent().hasClass('dice') ) {
      // select current number
      $('.dice .col-1').removeClass('sel');
      $(this).parent().parent().find('.col-1').addClass('sel');
    }
  });

  // ON DICE NUM CLICK
  $('.dice .col-1').click(function(){
    if( $(this).hasClass('sel_town') ) {
      $(this).removeClass('sel_town').addClass('sel_city');
    } else if( $(this).hasClass('sel_city') ) {
      $(this).removeClass('sel_city');
    } else {
      $(this).addClass('sel_town');
    }
  });

  $('input[name="css"]').focus(function(){
    $(this).select();
    document.execCommand("copy");
  });

  // IMG OVER
  function img_over(img) {
    var next_img = img.closest('.img').next();
    // console.log(next_img);
    if(next_img.length > 0 && next_img.hasClass('img')) {
      var filename = next_img.find('img').attr('title');
      // console.log(filename);
      var img_img = img.find('img');
      img_img.attr('data-src', img_img.attr('src') ).attr('src', 'images/'+filename);
    }
  }
  function img_out(img) {
    var img_img = img.find('img');
    if(img_img.attr('data-src') ){
      img_img.attr('src', img_img.attr('data-src'));
    }
  }
  // IMG DELETE click
  function img_delete(img) {
    var img_img = img.find('img');
    // var source = img_img.attr('src');
    var filename = img_img.attr('title');
    if(confirm('delete file: '+ filename +'?')){
      api('api.php?action=delete&filename='+filename, function(retour){
        if(retour[0] === true) {
          img.remove();
        }
      });

    }
  }
  // IMG DUPLICATE click
  function img_duplicate(img) {
    var img_img = img.find('img');
    var filename = img_img.attr('title');
    if(confirm('duplicate file: '+ filename +'?')){
      api('api.php?action=duplicate&filename='+filename, function(retour){
        // console.log(retour);
        if(retour[0] === true) {
          start_scan();
        }
      });

    }
  }
  function api(url, on_success = null, on_error = null){
    ajax_edit_ajax = $.ajax({
      url : url,
      type : 'GET',
      dataType : 'html',
      // data : data,
      success : function(retour_json){
        if(retour_json != ''){
          // console.log(retour_json);
          retour_json = JSON.parse(retour_json);
          if(on_success) on_success(retour_json);
        } else {
          console.log('error retour ajax');
        }
      },
      error : function(resultat, statut, erreur){
        console.log( 'Error: ', resultat);
      }
    });
  }

  var special_colors_web = ['d79e31','008ba9','458d32', '000000'];
  var special_colors_app =  ['d3a105','2c8bad','4a8f1b'];

  var special_dices = [2,3,4,5,6,7,8,9,10,11,12];

  var MODE = 'web';
  var MODE_determined = false;

  function determine_mode(col){
    let mode_temp = false;
    if(col != '000000') {
      mode_temp = ( $.inArray(col, special_colors_web) > -1 ) ? 'web' : false;
      if( mode_temp == false ) {
        mode_temp = ($.inArray(col, special_colors_app) > -1 ) ? 'app' : false;
      }
    }
    if(mode_temp != false) {
      MODE = mode_temp;
      MODE_determined = true;
    }
  }

  function traite_images(images){
    var html = '';
    var html_images = '';
    var num=0;
    var stats=[];
    var dices=[];

    var current_dice = 0;

    html_images+='<div class="list_images">';
    images.forEach(function(filename) {
      var filename_parts = filename.split('-');
      // var col_pos = filename.indexOf('-hex');
      // color = filename.substr(col_pos+4, 6);
      // console.log(filename_parts);
      if( filename_parts.length > 2 ) {
        color = filename_parts[2].substr(3, 6);
        if(stats[color]) stats[color]++;
        else stats[color]=1;
        if( ! MODE_determined) determine_mode(color);
      }


      let current_num = 0;
      if(filename_parts.length > 3) {
        var val = filename_parts[3].split('.')[0];
        if(dices[val]) dices[val]++;
        else dices[val]=1;
        current_num = val;
      }
      current_dice = (current_dice == 0) ? current_num : current_dice;

      num++;
      html_img_num = (current_num > 0) ? '<div class="num">'+ current_num +'</div>' : '';

      html_buts = '';
      html_buts+= '<div class="buts">';
      html_buts+= '<button type="button" class="btn btn-sm btn-danger but-delete"><span class="far fa-w fa-trash-alt" title="delete"></span></button><br>';
      html_buts+= '<button type="button" class="btn btn-sm btn-info but-duplicate"><span class="far fa-w fa-copy" title="duplicate"></span></button>';
      html_buts+= '</div>';

      if (current_num == 0) html_buts = '';

      html_images+= '<div class="img"><img class="img0" src="images/'+filename+'" alt="'+filename+'" title="'+filename+'">' + html_img_num + html_buts + '</div>';
      // html_images+= ( num == 1 ) ? '<br>':'';
    });
    html_images+='</div>'
    // console.log(dices);
    var tot_img = num;
    // html+= '<h3>Statistiques</h3>';
    var special_colors = (MODE=='app') ? special_colors_app : special_colors_web;
    // colors
    var tot = 0;
    var num = 0;
    special_colors.forEach(function(col) {
      let nb = stats[col];
      nb = (typeof nb === 'undefined') ? 0 : nb;
      stats[col] = nb;
      // html+= '<div class="color" style="background-color:#'+col+';">' + nb + '</div>';
      $('.com input').eq(num).val(nb).change();
      tot += nb;
      num++;
    });
    // console.log(stats);
    // // Quick n dirty hack for 'app' MODE
    // var num = 0;
    // special_colors_app.forEach(function(col) {
    //   let nb = stats[col];
    //   nb = (typeof nb === 'undefined') ? 0:nb;
    //   // html+= '<div class="color" style="background-color:#'+col+';">' + nb + '</div>';
    //   $('.com input').eq(num).val(nb).change();
    //   tot += nb;
    //   num++;
    // });

    // html+= ' = <strong>' + tot + '</strong>';
    // html += ' <small>(images: ' + images.length + ')</small>';

    // dices
    // html+= '<br><br>';
    special_dices.forEach(function(res) {
      let nb = dices[res];
      nb = (typeof nb === 'undefined') ? 0:nb;
      dices[res] = nb;
      // html+= '<div class="number">' + res + '<br><small>' + nb + '</small></div>';
      $('.dice input[name="d'+ res +'"]').val(nb).change();
    });

    $('.dice input[name="d'+ current_dice +'"]').change();

    // html+= ' = <strong>' + tot + '</strong>';
    // html+= '<hr>';
    var nb_robber = ( stats['000000'] != undefined ) ? stats['000000'] : 0;
    // console.log('nb_robber: '+nb_robber);
    if(MODE == 'app') {
      tot += nb_robber;
      $('.com input').eq(3).val(nb_robber).change();
    }
    var robber_coming = 7 - (nb_robber % 7);
    var robber_class = (robber_coming <= 3) ? 'bg-warning text-dark' : 'bg-secondary';
    robber_class = (robber_coming == 1) ? 'bg-danger' : robber_class;
    var plurial = (robber_coming > 1) ? 's' : '';

    html+= '<h'+ robber_coming +' class="robber_indic '+ robber_class +'">Robber coming in <stong>'+ robber_coming + '</strong> move'+ plurial +'</h'+ robber_coming +'>';
    html+= '<h3>Images (' + images.length + ', dices: <strong>'+ tot + '</strong>)</h3>';
    html+= html_images;
    $('.images').html(html);

    // actions
    var the_images = $('.list_images .img');//.not(':first');
    the_images.mouseover(function(){
      img_over($(this));
    });
    the_images.mouseout(function(){
      img_out($(this));
    });
    the_images.find('.buts .but-delete').click(function(){
      img_delete($(this).parent().parent());
    });
    the_images.find('.buts .but-duplicate').click(function(){
      img_duplicate($(this).parent().parent());
    });

    dices.splice(0,2);
    return dices;
  }

  // API SCAN FILES
  var current_nb_images = 0;
  var last_stats = [];

  function scan(){
    $('.icon_loading').show();
    api('api.php?action=files', function(images){
      if( Array.isArray(images) && images.length != current_nb_images) {
        last_stats = traite_images(images);
        if(last_stats.length > 0) update_stats_graph(last_stats);
      }
      $('.icon_loading').hide();
      current_nb_images = images.length;
    });
  }

  var timer;
  function start_scan(){
    clearInterval(timer);
    scan();
    timer = setInterval(function(){ scan(); }, scan_interval);
  }

  // Charts.js
  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };
  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };
  Chart.defaults.global.defaultFontColor = '#fff';
  Chart.defaults.global.defaultFontSize = 12;
  function update_stats_graph(last_stats){

    // console.log(last_stats);

    var ctx = document.getElementById('stats_graph').getContext('2d');
    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: special_dices,
        datasets: [{
          // legend: false,
          label: 'x',
          data: last_stats,//[12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2],
          // backgroundImage: 'url(background.jpg)',
          // backgroundPosition: 'bottom right',
          // backgroundRepeat: 'repeat-y',
          backgroundColor: '#a45633',
        }]
      },
      options: {
        scales: {
          xAxes: [{
            barPercentage: 1,
            categoryPercentage: 0.95,
            ticks: {
              // mirror: true,
            },
            gridLines: {
              display: true,
              color: '#333',
              offsetGridLines: true,
            },
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              max: last_stats.max(),
            },
            gridLines: {
              display: true,
              color: '#333',
              offsetGridLines: false,
            },
          }]
        },
        defaultFontColor: 'white',
        legend: {
          display: false,
          labels: {
            // This more specific font property overrides the global property
            fontColor: 'white',
          }
        },
        layout: {
          padding: {
          }
        }
      }
    });
  }


  $('.icon_loading').hide();
  start_scan();

});
