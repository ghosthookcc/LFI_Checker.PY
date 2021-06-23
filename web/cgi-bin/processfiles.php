<?php

class fileinfo
{

  function iterdir($dir)
  {
    global $fileiterator, $dirlen, $files;

    $files = array_filter(glob($dir . "/*"), "is_file");

    $fileiterator = new FilesystemIterator($dir, FilesystemIterator::SKIP_DOTS);
    $dirlen = iterator_count($fileiterator);

    function normalizeFiles($files, $str)
    {
      $newfiles = [];
      foreach($files as $itemtostrip)
      {
        array_push($newfiles, str_replace($str, "", $itemtostrip));
      }
      return $newfiles;
    }

    /*
    function getfilecontent($files)
    {
      $filecontent = [];

      foreach($files as $file)
      {
        $content = "";
        $filerw = fopen($file, "r+");
        while($line = fgets($filerw))
        {
          if($line == "<!DOCTYPE html>")
          {
            $content .= "HELLLLLLLLOOOOO" . $line;
          } else {
            $content .= "HELLO" . $line . "\n";
          }
        }
        fclose($filerw);
        array_push($filecontent, $content);
      }
      return $filecontent;
    }
    */

    function getfilecontent($files)
    {
      $filecontent = [];

      foreach($files as $file)
      {
        array_push($filecontent, file_get_contents($file));
      }

      return $filecontent;
    }

    function getfilenames($files)
    {
      $filenames = normalizeFiles($files, "200/");
      return $filenames;
    }

    function getfilextensions($files)
    {
      $filetypes = [];

      foreach($files as $filetype)
      {
        $splitdots = explode(".", $filetype);
        $extension = end($splitdots);
        array_push($filetypes, "." . $extension);
      }

      return $filetypes;
    }

    function getfilesizes($files, $byteform)
    {
      $filesizes = [];

      foreach($files as $filesize)
      {
        if($byteform == "byte")
        {
          array_push($filesizes, filesize($filesize) . "bytes");
        }
        else if($byteform == "kilobyte")
        {
          array_push($filesizes, round(filesize($filesize) / 1024, 3) . "kb");
        }
      }

      return $filesizes;
    }

    function testprint($files)
    {
      print_r(getfilenames($files));
      echo "<br>";
      print_r(getfilextensions($files));
      echo "<br>";
      print_r(getfilesizes($files, "kilobyte"));
    }

    $allinfo = [];

    $allinfo[0] = getfilenames($files);
    $allinfo[1] = getfilextensions($files);
    $allinfo[2] = getfilesizes($files, "kilobyte");
    $allinfo[3] = getfilecontent($files);

    return $allinfo;
  }

  function getUrls($file)
  {
    $split_content = [];
    if(file_exists($file))
    {
      $file_read = fopen($file, "r");
      while($line = fgets($file_read))
      {
        array_push($split_content, $line);
      }
      fclose($file_read);
    } 
    return $split_content;
  }
}

function addElement($dirlen, $names, $extensions, $sizes, $content)
{
  for($i = 0; $i < $dirlen; $i++)
  {
    echo "<div>";
    echo    "<pre>" . $names[$i] . "</pre>";
    echo    "<div class='itemInfo'>";
    echo      "<span>Type: " . $extensions[$i] . "</span><span>InfoFrom: " . "urls.txt" . "</span><span>Size: " . $sizes[$i] . "</span>";
    echo    "</div>";
    echo    "<div class='item'>";
    echo      "<summary>";
    echo        "<textarea>";
    echo          $content[$i];
    echo        "</textarea>";
    echo      "</summary>";
    echo    "</div>";
    echo "</div>";
  }
}

?>
