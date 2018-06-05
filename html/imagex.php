<?php
class ImageClass
{
    // property declaration
    public $imagename = 'name';
    public function displayName() {
        echo $this->var;
    }
    
}

header('Access-Control-Allow-Origin: *');

$files = array();



$dir_iterator = new RecursiveDirectoryIterator("img/");
$dir_iterator->setFlags(RecursiveDirectoryIterator::SKIP_DOTS);
$iterator = new RecursiveIteratorIterator($dir_iterator, RecursiveIteratorIterator::SELF_FIRST);
// could use CHILD_FIRST if you so wish

$filetypes = array("jpg");

foreach ($iterator as $file) {
    $filetype = pathinfo($file, PATHINFO_EXTENSION);
    if (in_array(strtolower($filetype), $filetypes)) {
        
        $f = new ImageClass();
        $f->imagename=$file->getFilename();
//        $f->videoname=str_replace(".jpg", ".h264", $file->getFilename());
       // $f->imagetime=date("Y-m-d-H-i-s", $file->getMTime());
        
        $files[] = $f;
    }
}

//asort($files);

header('Content-type: application/json');
echo json_encode($files);

?>

