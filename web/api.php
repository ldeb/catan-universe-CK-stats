<?php

function get_files(){
  $dir    = 'images/';
  // $files = scandir($dir, SCANDIR_SORT_DESCENDING);
  $files = array_diff(scandir($dir, SCANDIR_SORT_DESCENDING), array('..', '.'));
  return $files;
}
function delete_file($filename){
  $dir    = 'images/';
  return @unlink($dir.$filename);
}
function duplicate_file($filename){
  $dir    = 'images/';
  $filename_exploded = explode( '-', $filename);
  $filename_exploded[0] = ($filename_exploded[0] + 1);
  $new_filename = implode( '-', $filename_exploded);
  // return $filename.'___'.$new_filename;
  return @copy($dir.$filename, $dir.$new_filename);
}

$SHELL_PYTHON_PATH = "python"; //"/home/yacpve/.virtualenvs/pers2pict/bin/python";

if(isset($_GET['action'])) {
  switch($_GET['action']){
    case 'files' :
      echo json_encode(get_files());
      break;
    case 'delete' :
      if(isset($_GET['filename'])) {
        echo json_encode( [delete_file($_GET['filename'])] );
      }
      break;
    case 'duplicate' :
      if(isset($_GET['filename'])) {
        echo json_encode( [duplicate_file($_GET['filename'])] );
      }
      break;
    case 'start' :
      ////////////////////////////////////////////
      // PYTHON : ON LANCE LE SCRIPT  -   Not really reliable...
      ////////////////////////////////////////////
      $pyscript = 'C:\\users\\lolo8\\workspace\\python\\livecatan\\main.py';
      $python = 'C:\\Users\\Lolo8\\workspace\\python\\pyscreenshot\\venv\\Scripts\\python.exe';
      $action = '';
      $cmd = "$python $pyscript $action";
      $res = exec("$cmd", $output);
      $res = exec("s", $output);
      var_dump($res);
      var_dump($output);
      // echo json_encode( $output );
      break;

    default:
  }
}
