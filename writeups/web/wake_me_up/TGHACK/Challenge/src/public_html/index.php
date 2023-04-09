<?php 
class wakeMeUpBeforeYouGoGo {
  public $awake;
  function __destruct(){
    if ($this->awake == "no") {
	echo "You did not wake me up. Thank you!";
	echo "<br/>";
    	echo "The flag is: " . file_get_contents("/flag.txt");
    }
    else {
    	echo "I am awake.....";
    }
  }  
  
  function __wakeup(){
    $this->awake = "yes";
    echo "You woke me up!!!!!";
  }
}
highlight_file(__FILE__);
unserialize(base64_decode($_GET['wow']));
?>
