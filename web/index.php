<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>LiveCatan</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">

    <link href="inc/style.css" rel="stylesheet">

    <link rel="icon" type="image/png" href="inc/favicon-16x16.png" sizes="16x16">
    <link rel="icon" type="image/png" href="inc/favicon-32x32.png" sizes="32x32">
    <link rel="icon" type="image/png" href="inc/favicon-96x96.png" sizes="96x96">

  </head>

  <body class="dark">

    <div class="container-fluid">

      <h1 class="header-text text-light"><span class="icon_loading fas fa-sync-alt fa-spin mr-2"></span><a href="index.php">Catan Universe Stats 2019 &copy; faYa </a></h1>

      <div class="row">
        <div class="col-3 left-col">

          <!-- <p class="lead"></p> -->

          <h3>Dice</h3>
          <div class="dice">
            <?php for($i=2; $i<=12; $i++) : ?>
            <div class="row no-gutters0">
              <div class="col-1"><?=$i?></div>
              <div class="col"><input name="d<?=$i?>" type="number" step="1" min="0" value="0"><div class="bar">&nbsp;</div><div class="bar_legend"><?=$i?></div></div>
            </div>
          <?php endfor; ?>

          </div>
          <hr />

          <h3>Colors</h3>
          <div class="row com sheep no-gutters">
            <div class="col-1">&nbsp;</div>
            <div class="col"><input name="sheep" type="number" step="1" min="0" value="0"><div class="bar">&nbsp;</div></div>
          </div>
          <div class="row com rock no-gutters">
            <div class="col-1">&nbsp;</div>
            <div class="col"><input name="rock" type="number" step="1" min="0" value="0"><div class="bar">&nbsp;</div></div>
          </div>
          <div class="row com wood no-gutters">
            <div class="col-1">&nbsp;</div>
            <div class="col"><input name="wood" type="number" step="1" min="0" value="0"><div class="bar">&nbsp;</div></div>
          </div>
          <div class="row com robber no-gutters">
            <div class="col-1">&nbsp;</div>
            <div class="col"><input name="robber" type="number" step="1" min="0" value="0"><div class="bar">&nbsp;</div></div>
          </div>

          <div class="form-group mt-5">
            <input type="text" name="css" class="form-control form-control-sm bg-dark text-light" value="div.template-wrap{margin: 0 auto;} div.template-wrap, div.game-view {width: 100%;} div.game-container {height: 100%;} #footer,nav.navbar{display: none;}" title="to paste at the bottom of catanuniverse.com's style.css">
          </div>

        </div><!-- /col-1-->

        <div class="col images">
          <div class="list_images"></div>
        </div>

      </div><!-- /row-->
    </div>

    </div> <!-- /container -->

    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    <script src="inc/script.js"></script>

  </body>
</html>
